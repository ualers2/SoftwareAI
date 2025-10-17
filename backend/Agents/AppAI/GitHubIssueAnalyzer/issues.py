import asyncio
import aiohttp
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from agents import Agent, Runner, SQLiteSession
import base64
import json
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta



load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../', "Keys", "keys.env"))


class ProblemSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    BLOCKED = "blocked"


class Priority(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"


class Effort(Enum):
    S = "S"  # Small (1-2 dias)
    M = "M"  # Medium (3-5 dias)
    L = "L"  # Large (1-2 semanas)
    XL = "XL"  # Extra Large (2+ semanas)


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None


@dataclass 
class GitHubUser:
    login: str
    avatar_url: str
    html_url: str


@dataclass
class GitHubLabel:
    name: str
    color: str
    description: Optional[str] = None


@dataclass
class GitHubMilestone:
    title: str
    description: Optional[str]
    state: str
    due_on: Optional[datetime] = None


@dataclass
class GitHubIssue:
    number: int
    title: str
    body: Optional[str]
    state: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    labels: List[GitHubLabel]
    assignees: List[GitHubUser]
    milestone: Optional[GitHubMilestone]
    user: GitHubUser
    html_url: str
    comments: int

    def to_issue(self) -> 'Issue':
        """Converte GitHubIssue para Issue do nosso sistema."""
        # Mapear severidade baseado nas labels
        severity = self._map_severity()
        
        # Extrair tasks do corpo da issue (formato de checklist)
        tasks = self._extract_tasks_from_body()
        
        # Determinar componente baseado em labels ou título
        component = self._determine_component()
        
        return Issue(
            id=f"#{self.number}",
            title=self.title,
            description=self.body or "",
            severity=severity,
            status=self.state,
            created_date=self.created_at,
            tasks=tasks,
            labels=[label.name for label in self.labels],
            component=component,
            reporter=self.user.login
        )
    
    def _map_severity(self) -> ProblemSeverity:
        """Mapeia labels do GitHub para severidade."""
        label_names = [label.name.lower() for label in self.labels]
        
        if any(label in label_names for label in ['critical', 'urgent', 'blocker', 'p0']):
            return ProblemSeverity.CRITICAL
        elif any(label in label_names for label in ['high', 'important', 'p1']):
            return ProblemSeverity.HIGH
        elif any(label in label_names for label in ['medium', 'normal', 'p2']):
            return ProblemSeverity.MEDIUM
        else:
            return ProblemSeverity.LOW
    
    def _extract_tasks_from_body(self) -> List[Task]:
        """Extrai tasks de checklists no corpo da issue."""
        tasks = []
        if not self.body:
            return tasks
        
        lines = self.body.split('\n')
        task_counter = 1
        
        for line in lines:
            line = line.strip()
            
            # Detectar checkboxes: - [ ] ou - [x] ou * [ ] ou * [x]
            if line.startswith(('- [ ]', '- [x]', '* [ ]', '* [x]', '+ [ ]', '+ [x]')):
                is_completed = '[x]' in line.lower() or '[X]' in line
                task_title = line[5:].strip()  # Remove "- [x] "
                
                if task_title:
                    status = TaskStatus.COMPLETED if is_completed else TaskStatus.PENDING
                    
                    tasks.append(Task(
                        id=f"T{task_counter:03d}",
                        title=task_title,
                        description="",
                        status=status
                    ))
                    task_counter += 1
        
        return tasks
    
    def _determine_component(self) -> Optional[str]:
        """Determina componente baseado em labels e título."""
        label_names = [label.name.lower() for label in self.labels]
        title_lower = self.title.lower()
        
        # Mapeamento de labels/palavras-chave para componentes
        component_mapping = {
            'frontend': ['frontend', 'ui', 'ux', 'react', 'vue', 'angular', 'css', 'html', 'javascript'],
            'backend': ['backend', 'api', 'server', 'database', 'db', 'sql', 'auth', 'authentication'],
            'mobile': ['mobile', 'ios', 'android', 'flutter', 'react-native'],
            'infra': ['infrastructure', 'devops', 'docker', 'kubernetes', 'deployment', 'ci/cd'],
            'security': ['security', 'vulnerability', 'auth', 'ssl', 'encryption'],
            'performance': ['performance', 'slow', 'optimization', 'memory', 'cpu'],
            'docs': ['documentation', 'docs', 'readme', 'guide']
        }
        
        for component, keywords in component_mapping.items():
            if any(keyword in label_names for keyword in keywords) or \
               any(keyword in title_lower for keyword in keywords):
                return component.title()
        
        return None


@dataclass
class Issue:
    id: str
    title: str
    description: str
    severity: ProblemSeverity
    status: str
    created_date: datetime
    tasks: List[Task]
    labels: List[str]
    component: Optional[str] = None
    reporter: Optional[str] = None


# === GITHUB INTEGRATION ===

class GitHubClient:
    """Cliente para interagir com a API do GitHub."""
    
    def __init__(self, token: str, owner: str, repo: str):
        """
        Inicializa o cliente GitHub.
        
        Args:
            token: Personal Access Token do GitHub
            owner: Dono do repositório (username ou org)
            repo: Nome do repositório
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ProblemAnalyzer/1.0"
        }
    
    async def get_issues(self, 
                        state: str = "open",
                        labels: Optional[str] = None,
                        milestone: Optional[str] = None,
                        assignee: Optional[str] = None,
                        since: Optional[datetime] = None,
                        per_page: int = 100) -> List[GitHubIssue]:
        """
        Busca issues do repositório.
        
        Args:
            state: Estado das issues ('open', 'closed', 'all')
            labels: Labels filtrar (comma-separated)
            milestone: Milestone para filtrar
            assignee: Usuário assignado para filtrar
            since: Data mínima de criação
            per_page: Número de issues por página
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        
        params = {
            "state": state,
            "per_page": per_page,
            "sort": "updated",
            "direction": "desc"
        }
        
        if labels:
            params["labels"] = labels
        if milestone:
            params["milestone"] = milestone
        if assignee:
            params["assignee"] = assignee
        if since:
            params["since"] = since.isoformat()
        
        issues = []
        page = 1
        
        async with aiohttp.ClientSession() as session:
            while True:
                params["page"] = page
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 401:
                        raise Exception("GitHub token inválido ou sem permissões")
                    elif response.status == 404:
                        raise Exception(f"Repositório {self.owner}/{self.repo} não encontrado")
                    elif response.status != 200:
                        raise Exception(f"Erro na API GitHub: {response.status}")
                    
                    data = await response.json()
                    
                    if not data:  # Não há mais páginas
                        break
                    
                    for issue_data in data:
                        # Filtrar pull requests (GitHub API retorna PRs como issues)
                        if "pull_request" not in issue_data:
                            issue = self._parse_issue(issue_data)
                            issues.append(issue)
                    
                    # Se retornou menos que per_page, não há mais páginas
                    if len(data) < per_page:
                        break
                    
                    page += 1
        
        return issues
    
    async def get_issue(self, issue_number: int) -> GitHubIssue:
        """Busca uma issue específica."""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Erro ao buscar issue #{issue_number}: {response.status}")
                
                data = await response.json()
                return self._parse_issue(data)
    
    async def get_repository_info(self) -> Dict[str, Any]:
        """Obtém informações básicas do repositório."""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Erro ao buscar repositório: {response.status}")
                
                return await response.json()
    
    def _parse_issue(self, data: Dict[str, Any]) -> GitHubIssue:
        """Converte dados JSON da API em GitHubIssue."""
        
        # Parse labels
        labels = [
            GitHubLabel(
                name=label["name"],
                color=label["color"],
                description=label.get("description")
            )
            for label in data.get("labels", [])
        ]
        
        # Parse assignees
        assignees = [
            GitHubUser(
                login=assignee["login"],
                avatar_url=assignee["avatar_url"],
                html_url=assignee["html_url"]
            )
            for assignee in data.get("assignees", [])
        ]
        
        # Parse milestone
        milestone = None
        if data.get("milestone"):
            milestone_data = data["milestone"]
            due_on = None
            if milestone_data.get("due_on"):
                due_on = datetime.fromisoformat(milestone_data["due_on"].replace('Z', '+00:00'))
            
            milestone = GitHubMilestone(
                title=milestone_data["title"],
                description=milestone_data.get("description"),
                state=milestone_data["state"],
                due_on=due_on
            )
        
        # Parse user
        user = GitHubUser(
            login=data["user"]["login"],
            avatar_url=data["user"]["avatar_url"],
            html_url=data["user"]["html_url"]
        )
        
        # Parse dates
        created_at = datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(data["updated_at"].replace('Z', '+00:00'))
        closed_at = None
        if data.get("closed_at"):
            closed_at = datetime.fromisoformat(data["closed_at"].replace('Z', '+00:00'))
        
        return GitHubIssue(
            number=data["number"],
            title=data["title"],
            body=data.get("body"),
            state=data["state"],
            created_at=created_at,
            updated_at=updated_at,
            closed_at=closed_at,
            labels=labels,
            assignees=assignees,
            milestone=milestone,
            user=user,
            html_url=data["html_url"],
            comments=data.get("comments", 0)
        )

class IdentifiedProblem(BaseModel):
    """Problema identificado na issue."""
    category: str = Field(description="Categoria do problema (técnico, processo, design, etc.)")
    description: str = Field(description="Descrição detalhada do problema")
    impact: str = Field(description="Impacto do problema na aplicação")
    evidence: str = Field(description="Evidência ou indicador que aponta para este problema")


class RootCause(BaseModel):
    """Causa raiz de um problema."""
    cause: str = Field(description="Descrição da causa raiz")
    contributing_factors: List[str] = Field(description="Fatores que contribuem para esta causa")
    likelihood: str = Field(description="Probabilidade desta ser a causa real (alta/media/baixa)")


class Recommendation(BaseModel):
    """Recomendação de melhoria."""
    title: str = Field(description="Título da recomendação")
    description: str = Field(description="Descrição detalhada da recomendação")
    category: str = Field(description="Categoria (arquitetura, código, processo, etc.)")
    expected_benefit: str = Field(description="Benefício esperado com a implementação")
    implementation_notes: str = Field(description="Notas sobre como implementar")


class PriorityAction(BaseModel):
    """Ação prioritária a ser tomada."""
    action: str = Field(description="Ação específica a ser tomada")
    priority: Priority = Field(description="Nível de prioridade")
    effort: Effort = Field(description="Esforço estimado")
    responsible: str = Field(description="Quem deve executar esta ação")
    dependencies: List[str] = Field(default_factory=list, description="Dependências desta ação")


class ProblemAnalysis(BaseModel):
    """Análise estruturada de um problema/issue."""
    issue_id: str = Field(description="ID da issue analisada")
    analysis_summary: str = Field(description="Resumo executivo da análise")
    identified_problems: List[IdentifiedProblem] = Field(description="Problemas identificados")
    root_causes: List[RootCause] = Field(description="Possíveis causas raiz")
    recommendations: List[Recommendation] = Field(description="Recomendações de melhoria")
    priority_actions: List[PriorityAction] = Field(description="Ações prioritárias")
    technical_debt_score: int = Field(ge=1, le=10, description="Score de débito técnico (1-10)")
    risk_assessment: str = Field(description="Avaliação de riscos se não resolver")
    estimated_resolution_time: str = Field(description="Tempo estimado para resolução completa")


class RoadmapItem(BaseModel):
    """Item do roadmap de melhorias."""
    title: str = Field(description="Título do item")
    description: str = Field(description="Descrição detalhada")
    priority: Priority = Field(description="Prioridade")
    effort: Effort = Field(description="Esforço estimado")
    expected_impact: str = Field(description="Impacto esperado")
    dependencies: List[str] = Field(default_factory=list, description="Dependências")
    success_criteria: List[str] = Field(description="Critérios de sucesso")


class RoadmapPhase(BaseModel):
    """Fase do roadmap."""
    phase_name: str = Field(description="Nome da fase")
    duration: str = Field(description="Duração estimada da fase")
    objective: str = Field(description="Objetivo principal da fase")
    items: List[RoadmapItem] = Field(description="Itens desta fase")


class ImprovementRoadmap(BaseModel):
    """Roadmap de melhorias estruturado."""
    summary: str = Field(description="Resumo executivo do roadmap")
    total_estimated_duration: str = Field(description="Duração total estimada")
    phases: List[RoadmapPhase] = Field(description="Fases do roadmap")
    success_metrics: List[str] = Field(description="Métricas para medir sucesso")
    risks_and_mitigation: List[str] = Field(description="Riscos identificados e mitigação")


class Pattern(BaseModel):
    """Padrão identificado."""
    pattern_type: str = Field(description="Tipo de padrão (técnico, processo, temporal, etc.)")
    description: str = Field(description="Descrição do padrão")
    frequency: str = Field(description="Frequência de ocorrência")
    affected_components: List[str] = Field(description="Componentes afetados")
    impact: str = Field(description="Impacto do padrão")
    root_cause: str = Field(description="Causa raiz provável do padrão")


class SystemicRecommendation(BaseModel):
    """Recomendação sistêmica."""
    title: str = Field(description="Título da recomendação")
    description: str = Field(description="Descrição detalhada")
    target_patterns: List[str] = Field(description="Padrões que esta recomendação resolve")
    implementation_approach: str = Field(description="Abordagem de implementação")
    expected_outcomes: List[str] = Field(description="Resultados esperados")
    effort_required: Effort = Field(description="Esforço necessário")


class PatternAnalysis(BaseModel):
    """Análise de padrões entre issues."""
    analysis_summary: str = Field(description="Resumo da análise de padrões")
    identified_patterns: List[Pattern] = Field(description="Padrões identificados")
    systemic_recommendations: List[SystemicRecommendation] = Field(description="Recomendações sistêmicas")
    prevention_strategies: List[str] = Field(description="Estratégias para prevenir problemas recorrentes")
    process_improvements: List[str] = Field(description="Melhorias no processo de desenvolvimento")


# === STRUCTURED OUTPUT MODELS ===

class ProblemAnalyzerAgent:
    def __init__(self, github_token, github_owner, github_repo, session_id: str = "problem_analyzer"):
        """Inicializa o agente de análise de problemas com structured output."""
        
        # GitHub client (opcional)
        self.github_client = None
        if github_token and github_owner and github_repo:
            self.github_client = GitHubClient(github_token, github_owner, github_repo)
        
        # Agente para análise individual de issues
        self.analysis_agent = Agent(
            name="ProblemAnalyzer",
            model="gpt-5-nano",
            instructions="""
            Você é um especialista sênior em análise de problemas e qualidade de software.
            
            Analise issues detalhadamente e identifique:
            1. Problemas específicos (técnicos, de processo, de design)
            2. Causas raiz prováveis com evidências
            3. Recomendações acionáveis e específicas
            4. Ações prioritárias organizadas por impacto
            5. Score de débito técnico baseado em complexidade e risco
            
            Seja específico, prático e baseie-se em melhores práticas da indústria.
            Considere: performance, segurança, manutenibilidade, escalabilidade, UX.
            
            Para cada problema identificado, forneça evidências concretas.
            Para cada recomendação, inclua benefícios esperados e notas de implementação.
            """,
            output_type=ProblemAnalysis
        )
        
        # Agente para roadmap de melhorias
        self.roadmap_agent = Agent(
            name="RoadmapGenerator",
            model="gpt-5-nano",
            instructions="""
            Você é um especialista em planejamento estratégico de melhorias técnicas.
            
            Crie roadmaps estruturados em fases:
            1. Sprint Atual (1-2 semanas) - ações críticas e quick wins
            2. Próximo Sprint (2-4 semanas) - melhorias importantes
            3. Longo Prazo (1-3 meses) - refatorações e mudanças estruturais
            
            Para cada item:
            - Priorize por impacto vs esforço
            - Defina critérios de sucesso mensuráveis
            - Identifique dependências e riscos
            - Estime esforços realisticamente
            
            Mantenha o foco em value delivery e ROI.
            """,
            output_type=ImprovementRoadmap
        )
        
        # Agente para análise de padrões
        self.pattern_agent = Agent(
            name="PatternAnalyzer",
            model="gpt-5-nano",
            instructions="""
            Você é um especialista em identificação de padrões e melhorias sistêmicas.
            
            Identifique padrões recorrentes:
            1. Padrões Técnicos - tipos de bugs, problemas de arquitetura
            2. Padrões de Processo - gargalos, falhas de comunicação
            3. Padrões Temporais - quando problemas ocorrem
            4. Padrões de Componentes - áreas mais problemáticas
            
            Para cada padrão:
            - Determine frequência e impacto
            - Identifique causa raiz sistêmica
            - Proponha soluções preventivas
            
            Foque em melhorias que quebrem ciclos viciosos e previnam problemas futuros.
            """,
            output_type=PatternAnalysis
        )
        
        self.session = SQLiteSession(session_id, "problem_analysis.db")
    
    def to_aware_utc(self, dt: Optional[datetime]) -> Optional[datetime]:
        """Garante que dt seja timezone-aware em UTC. Se dt for None, retorna None."""
        if dt is None:
            return None
        if dt.tzinfo is None:
            # assumir que datetimes sem tz são UTC (ou ajuste para sua timezone se preferir)
            return dt.replace(tzinfo=timezone.utc)
        # converte para UTC caso tenha outro offset
        return dt.astimezone(timezone.utc)

    async def fetch_github_issues(self, 
                                 state: str = "open",
                                 labels: Optional[str] = None,
                                 days_back: int = 30) -> List[Issue]:
        """
        Busca issues do GitHub e converte para o formato interno.
        
        Args:
            state: Estado das issues ('open', 'closed', 'all')
            labels: Labels para filtrar (comma-separated)
            days_back: Buscar issues dos últimos N dias
        """
        if not self.github_client:
            raise Exception("GitHub client não configurado. Forneça token, owner e repo.")
                
        since = None
        if days_back and days_back > 0:
            since = datetime.now(timezone.utc) - timedelta(days=days_back)
            # opcional: truncar para início do dia UTC
            since = since.replace(hour=0, minute=0, second=0, microsecond=0)

        try:
            github_issues = await self.github_client.get_issues(
                state=state,
                labels=labels,
                since=since
            )
            
            # Converter para formato interno
            issues = []
            for gh_issue in github_issues:
                issue = gh_issue.to_issue()
                issues.append(issue)
            
            return issues
        
        except Exception as e:
            raise Exception(f"Erro ao buscar issues do GitHub: {str(e)}")
    
    async def analyze_repository(self, 
                               state: str = "open",
                               labels: Optional[str] = None,
                               days_back: int = 30) -> Dict[str, Any]:
        """
        Analisa todas as issues de um repositório GitHub.
        
        Returns:
            Dicionário com análises completas, roadmap e padrões
        """
        if not self.github_client:
            raise Exception("GitHub client não configurado.")
        
        print(f"🔍 Buscando issues do repositório {self.github_client.owner}/{self.github_client.repo}...")
        
        # Buscar issues do GitHub
        issues = await self.fetch_github_issues(state=state, labels=labels, days_back=days_back)
        
        if not issues:
            return {
                "message": "Nenhuma issue encontrada com os filtros especificados",
                "repository": f"{self.github_client.owner}/{self.github_client.repo}",
                "filters": {"state": state, "labels": labels, "days_back": days_back}
            }
        
        print(f"✅ Encontradas {len(issues)} issues. Iniciando análise...")
        
        # Analisar cada issue
        analyses = []
        for i, issue in enumerate(issues, 1):
            print(f"📋 Analisando issue {i}/{len(issues)}: {issue.id}")
            analysis = await self.analyze_issue(issue)
            analyses.append(analysis)
        
        print("🗺️ Gerando roadmap de melhorias...")
        roadmap = await self.generate_improvement_roadmap(analyses)
        
        print("🔄 Identificando padrões...")
        patterns = await self.identify_patterns(issues)
        
        # Estatísticas do repositório
        repo_stats = await self._generate_repository_stats(issues, analyses)
        
        return {
            "repository": f"{self.github_client.owner}/{self.github_client.repo}",
            "analysis_date": datetime.now(timezone.utc).isoformat(),
            "filters": {"state": state, "labels": labels, "days_back": days_back},
            "statistics": repo_stats,
            "individual_analyses": analyses,
            "improvement_roadmap": roadmap,
            "pattern_analysis": patterns
        }
    
    async def _generate_repository_stats(self, issues: List[Issue], analyses: List[ProblemAnalysis]) -> Dict[str, Any]:
        """Gera estatísticas do repositório."""
        total_issues = len(issues)
        
        # Estatísticas por severidade
        severity_stats = {}
        for issue in issues:
            sev = issue.severity.value
            severity_stats[sev] = severity_stats.get(sev, 0) + 1
        
        # Estatísticas por componente
        component_stats = {}
        for issue in issues:
            comp = issue.component or "Unknown"
            component_stats[comp] = component_stats.get(comp, 0) + 1
        
        # Estatísticas de débito técnico
        debt_scores = [a.technical_debt_score for a in analyses]
        avg_debt_score = sum(debt_scores) / len(debt_scores) if debt_scores else 0
        
        # Issues com tasks
        issues_with_tasks = [i for i in issues if i.tasks]
        total_tasks = sum(len(i.tasks) for i in issues)
        completed_tasks = sum(len([t for t in i.tasks if t.status == TaskStatus.COMPLETED]) for i in issues)
        
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Ações de alta prioridade
        high_priority_actions = sum(
            len([a for a in analysis.priority_actions if a.priority == Priority.ALTA]) 
            for analysis in analyses
        )
        
        return {
            "total_issues": total_issues,
            "severity_distribution": severity_stats,
            "component_distribution": component_stats,
            "average_technical_debt": round(avg_debt_score, 1),
            "issues_with_tasks": len(issues_with_tasks),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "task_completion_rate": round(task_completion_rate, 1),
            "high_priority_actions": high_priority_actions,
            "total_recommendations": sum(len(a.recommendations) for a in analyses)
        }
    
    async def analyze_issue(self, issue: Issue) -> ProblemAnalysis:
        """Analisa uma issue e retorna análise estruturada."""
        
        context = self._prepare_analysis_context(issue)
        
        analysis_prompt = f"""
        Analise a seguinte issue detalhadamente:
        
        {context}
        
        Forneça uma análise completa e estruturada considerando todos os aspectos 
        técnicos, de processo e de negócio envolvidos.
        """
        
        result = await Runner.run(
            self.analysis_agent,
            analysis_prompt,
            session=self.session
        )
        
        return result.final_output  # Já é um ProblemAnalysis estruturado
    
    async def generate_improvement_roadmap(self, analyses: List[ProblemAnalysis]) -> ImprovementRoadmap:
        """Gera roadmap estruturado baseado nas análises."""
        
        summary = self._format_analyses_for_roadmap(analyses)
        
        roadmap_prompt = f"""
        Com base nas seguintes análises de problemas, crie um roadmap estruturado:
        
        {summary}
        
        Organize as melhorias em fases claras com objetivos mensuráveis.
        Priorize ações que resolvam múltiplos problemas simultaneamente.
        """
        
        result = await Runner.run(
            self.roadmap_agent,
            roadmap_prompt,
            session=self.session
        )
        
        return result.final_output  # Já é um ImprovementRoadmap estruturado
    
    async def identify_patterns(self, issues: List[Issue]) -> PatternAnalysis:
        """Identifica padrões estruturados entre issues."""
        
        context = self._format_issues_for_pattern_analysis(issues)
        
        patterns_prompt = f"""
        Analise as seguintes issues e identifique padrões sistêmicos:
        
        {context}
        
        Foque em padrões que, se resolvidos, podem prevenir problemas futuros 
        similares e melhorar a qualidade geral do sistema.
        """
        
        result = await Runner.run(
            self.pattern_agent,
            patterns_prompt,
            session=self.session
        )
        
        return result.final_output  # Já é um PatternAnalysis estruturado
    
    def _prepare_analysis_context(self, issue: Issue) -> str:
        """Prepara o contexto da issue para análise."""
        completed_tasks = [t for t in issue.tasks if t.status == TaskStatus.COMPLETED]
        pending_tasks = [t for t in issue.tasks if t.status != TaskStatus.COMPLETED]
        blocked_tasks = [t for t in issue.tasks if t.status == TaskStatus.BLOCKED]
        
        # Calcular métricas
        completion_rate = len(completed_tasks) / len(issue.tasks) * 100 if issue.tasks else 0
        now = datetime.now(timezone.utc)
        created = self.to_aware_utc(issue.created_date)
        days_open = (now - created).days if created else None

        # Calcular eficiência (estimado vs real)
        efficiency_info = ""
        total_estimated = sum(t.estimated_hours or 0 for t in completed_tasks)
        total_actual = sum(t.actual_hours or 0 for t in completed_tasks if t.actual_hours)
        
        if total_estimated > 0 and total_actual > 0:
            efficiency = (total_estimated / total_actual) * 100
            efficiency_info = f"\n**Eficiência**: {efficiency:.0f}% (Est: {total_estimated}h, Real: {total_actual}h)"
        
        context = f"""
        **ISSUE**: {issue.title}
        **ID**: {issue.id}
        **Severidade**: {issue.severity.value}
        **Status**: {issue.status}
        **Componente**: {issue.component or 'Não especificado'}
        **Criado em**: {issue.created_date.strftime('%Y-%m-%d')} ({days_open} dias atrás)
        **Labels**: {', '.join(issue.labels) if issue.labels else 'Nenhuma'}
        **Taxa de Conclusão**: {completion_rate:.0f}% ({len(completed_tasks)}/{len(issue.tasks)} tasks){efficiency_info}
        
        **Descrição**:
        {issue.description}
        
        **Tasks Completadas** ({len(completed_tasks)} de {len(issue.tasks)}):
        """
        
        for task in completed_tasks:
            hours_info = ""
            if task.estimated_hours and task.actual_hours:
                variance = ((task.actual_hours - task.estimated_hours) / task.estimated_hours) * 100
                hours_info = f" (Est: {task.estimated_hours}h, Real: {task.actual_hours}h, Variação: {variance:+.0f}%)"
            elif task.estimated_hours:
                hours_info = f" (Est: {task.estimated_hours}h)"
            
            context += f"✅ {task.title}{hours_info}\n"
            if task.description:
                context += f"   └─ {task.description}\n"
        
        if blocked_tasks:
            context += f"\n**Tasks Bloqueadas** ({len(blocked_tasks)}):\n"
            for task in blocked_tasks:
                context += f"🚫 {task.title}\n"
                if task.description:
                    context += f"   └─ {task.description}\n"
        
        pending_normal = [t for t in pending_tasks if t.status != TaskStatus.BLOCKED]
        if pending_normal:
            context += f"\n**Tasks Pendentes** ({len(pending_normal)}):\n"
            for task in pending_normal:
                status_icon = "🔄" if task.status == TaskStatus.IN_PROGRESS else "⏳"
                context += f"{status_icon} {task.title} [{task.status.value}]\n"
                if task.description:
                    context += f"   └─ {task.description}\n"
        
        return context
    
    def _format_analyses_for_roadmap(self, analyses: List[ProblemAnalysis]) -> str:
        """Formata análises para geração de roadmap."""
        summary = f"**RESUMO DE {len(analyses)} ANÁLISES**\n\n"
        
        # Estatísticas gerais
        avg_debt_score = sum(a.technical_debt_score for a in analyses) / len(analyses)
        high_priority_actions = sum(len([p for p in a.priority_actions if p.priority == Priority.ALTA]) for a in analyses)
        
        summary += f"**Métricas Gerais**:\n"
        summary += f"- Score médio de débito técnico: {avg_debt_score:.1f}/10\n"
        summary += f"- Total de ações de alta prioridade: {high_priority_actions}\n"
        summary += f"- Total de recomendações: {sum(len(a.recommendations) for a in analyses)}\n\n"
        
        for analysis in analyses:
            summary += f"""**Issue {analysis.issue_id}**:
- Resumo: {analysis.analysis_summary}
- Débito Técnico: {analysis.technical_debt_score}/10
- Tempo de Resolução: {analysis.estimated_resolution_time}
- Riscos: {analysis.risk_assessment}

**Top Recomendações**:
"""
            for rec in analysis.recommendations[:2]:  # Top 2
                summary += f"  • {rec.title}: {rec.expected_benefit}\n"
            
            summary += f"\n**Ações Prioritárias**:\n"
            for action in analysis.priority_actions[:3]:  # Top 3
                summary += f"  • [{action.priority.value}] {action.action} (Esforço: {action.effort.value})\n"
            
            summary += "\n"
        
        return summary
    
    def _format_issues_for_pattern_analysis(self, issues: List[Issue]) -> str:
        """Formata issues para análise de padrões."""
        summary = f"**ANÁLISE DE PADRÕES - {len(issues)} ISSUES**\n\n"
        
        # Estatísticas por severidade
        severity_counts = {}
        component_counts = {}
        label_counts = {}
        
        for issue in issues:
            severity_counts[issue.severity.value] = severity_counts.get(issue.severity.value, 0) + 1
            if issue.component:
                component_counts[issue.component] = component_counts.get(issue.component, 0) + 1
            for label in issue.labels:
                label_counts[label] = label_counts.get(label, 0) + 1
        
        summary += "**Distribuição por Severidade**:\n"
        for sev, count in severity_counts.items():
            summary += f"- {sev}: {count} issues\n"
        
        summary += "\n**Componentes Mais Afetados**:\n"
        for comp, count in sorted(component_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            summary += f"- {comp}: {count} issues\n"
        
        summary += "\n**Labels Mais Frequentes**:\n"
        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            summary += f"- {label}: {count} occurrences\n"
        
        summary += "\n**Detalhes das Issues**:\n"
        
        for issue in issues:
            task_completion = len([t for t in issue.tasks if t.status == TaskStatus.COMPLETED]) / len(issue.tasks) * 100 if issue.tasks else 0
            now = datetime.now(timezone.utc)
            created = self.to_aware_utc(issue.created_date)
            days_open = (now - created).days if created else None

            summary += f"""
**{issue.id}**: {issue.title}
- Severidade: {issue.severity.value} | Componente: {issue.component or 'N/A'}
- Labels: {', '.join(issue.labels) if issue.labels else 'N/A'}
- Progresso: {task_completion:.0f}% | Idade: {days_open} dias
- Descrição resumida: {issue.description[:200]}...

"""
        return summary


# === EXEMPLO COM GITHUB INTEGRATION ===

async def main():
    """Demonstração completa com integração GitHub."""
    
    # Configuração do GitHub (substitua pelos seus dados)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Personal Access Token
    GITHUB_OWNER = "SoftwareAI-Company"            # Username ou org
    GITHUB_REPO = "MediaCutsStudio"              # Nome do repositório
    
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_TOKEN não encontrado nas variáveis de ambiente.")
        print("Para usar integração GitHub:")
        print("1. Crie um Personal Access Token em: https://github.com/settings/tokens")
        print("2. Configure as permissões: repo, read:user, read:project")
        print("3. Export GITHUB_TOKEN=seu_token")
        print("\n🔄 Executando exemplo com dados simulados...")
        await main_with_sample_data()
        return
    
    # Inicializar agente com GitHub
    analyzer = ProblemAnalyzerAgent(
        github_token=GITHUB_TOKEN,
        github_owner=GITHUB_OWNER,
        github_repo=GITHUB_REPO,
        session_id="github_analyzer"
    )
    
    print("🚀 ANÁLISE DE REPOSITÓRIO GITHUB")
    print("=" * 60)
    print(f"📁 Repositório: {GITHUB_OWNER}/{GITHUB_REPO}")
    
    try:
        # Analisar repositório completo
        results = await analyzer.analyze_repository(
            state="open",           # Issues abertas
            labels=None,            # Todas as labels
            days_back=300            # Últimos 300 dias
        )
        
        print("\n📊 ESTATÍSTICAS DO REPOSITÓRIO")
        print("=" * 40)
        stats = results["statistics"]
        print(f"📋 Total de issues: {stats['total_issues']}")
        print(f"📈 Débito técnico médio: {stats['average_technical_debt']}/10")
        print(f"✅ Taxa de conclusão de tasks: {stats['task_completion_rate']}%")
        print(f"🚨 Ações de alta prioridade: {stats['high_priority_actions']}")
        print(f"💡 Total de recomendações: {stats['total_recommendations']}")
        
        print("\n🎯 DISTRIBUIÇÃO POR SEVERIDADE")
        for severity, count in stats["severity_distribution"].items():
            print(f"  {severity}: {count} issues")
        
        print("\n🏗️ DISTRIBUIÇÃO POR COMPONENTE")
        for component, count in stats["component_distribution"].items():
            print(f"  {component}: {count} issues")
        
        # Mostrar primeira análise
        if results["individual_analyses"]:
            first_analysis = results["individual_analyses"][0]
            print(f"\n🔍 PRIMEIRA ANÁLISE - Issue {first_analysis.issue_id}")
            print("=" * 40)
            print(f"📝 Resumo: {first_analysis.analysis_summary}")
            print(f"📊 Score técnico: {first_analysis.technical_debt_score}/10")
            print(f"⏱️ Tempo estimado: {first_analysis.estimated_resolution_time}")
            
            if first_analysis.priority_actions:
                print(f"\n🚀 Primeira ação prioritária:")
                action = first_analysis.priority_actions[0]
                print(f"  • [{action.priority.value}] {action.action}")
                print(f"  • Esforço: {action.effort.value}")
                print(f"  • Responsável: {action.responsible}")
        
        # Mostrar roadmap
        roadmap = results["improvement_roadmap"]
        print(f"\n🗺️ ROADMAP DE MELHORIAS")
        print("=" * 40)
        print(f"📅 Duração total: {roadmap.total_estimated_duration}")
        print(f"🎯 Fases: {len(roadmap.phases)}")
        
        if roadmap.phases:
            print(f"\n🚀 Primeira fase: {roadmap.phases[0].phase_name}")
            print(f"  • Duração: {roadmap.phases[0].duration}")
            print(f"  • Objetivo: {roadmap.phases[0].objective}")
            print(f"  • Itens: {len(roadmap.phases[0].items)}")
        
        # Mostrar padrões
        patterns = results["pattern_analysis"]
        print(f"\n🔄 PADRÕES IDENTIFICADOS")
        print("=" * 40)
        print(f"🔍 Padrões encontrados: {len(patterns.identified_patterns)}")
        print(f"💡 Recomendações sistêmicas: {len(patterns.systemic_recommendations)}")
        
        if patterns.identified_patterns:
            print(f"\n🔍 Primeiro padrão:")
            pattern = patterns.identified_patterns[0]
            print(f"  • Tipo: {pattern.pattern_type}")
            print(f"  • Frequência: {pattern.frequency}")
            print(f"  • Componentes: {', '.join(pattern.affected_components[:3])}")
        
        # Exportar resultados
        output_file = f"analysis_{GITHUB_OWNER}_{GITHUB_REPO}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        # Converter Pydantic models para dict para serialização JSON
        export_data = {
            "repository": results["repository"],
            "analysis_date": results["analysis_date"],
            "filters": results["filters"],
            "statistics": results["statistics"],
            "individual_analyses": [a.model_dump() for a in results["individual_analyses"]],
            "improvement_roadmap": results["improvement_roadmap"].model_dump(),
            "pattern_analysis": results["pattern_analysis"].model_dump()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Análise exportada para: {output_file}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {str(e)}")
        print("\n🔄 Executando exemplo com dados simulados...")
        await main_with_sample_data()


async def main_with_sample_data():
    """Demonstração com dados simulados quando GitHub não está disponível."""
    
    # Criar issues de exemplo
    sample_issues = [
        Issue(
            id="ISSUE-001",
            title="Performance lenta no carregamento da dashboard",
            description="""
            A dashboard principal está levando mais de 10 segundos para carregar.
            Usuários reportando timeout em horários de pico.
            
            Contexto:
            - Ocorre principalmente entre 9h-11h e 14h-16h
            - Afeta ~500 usuários diariamente
            - Dashboard carrega 15 widgets diferentes
            - Cada widget faz query separada ao banco
            - Sem cache implementado
            - Queries N+1 identificadas
            """,
            severity=ProblemSeverity.HIGH,
            status="In Progress",
            created_date=datetime(2024, 8, 15),
            component="Frontend/Dashboard",
            labels=["performance", "database", "user-experience"],
            tasks=[
                Task("T001", "Analisar queries do banco", "Identificar queries lentas", TaskStatus.COMPLETED, estimated_hours=8, actual_hours=12),
                Task("T002", "Implementar cache Redis", "Cache para dados estáticos", TaskStatus.COMPLETED, estimated_hours=16, actual_hours=18),
                Task("T003", "Otimizar componentes React", "Lazy loading dos widgets", TaskStatus.IN_PROGRESS, estimated_hours=24),
                Task("T004", "Implementar paginação", "Paginar dados grandes", TaskStatus.PENDING, estimated_hours=12),
                Task("T005", "Monitoramento de performance", "Adicionar métricas", TaskStatus.BLOCKED, estimated_hours=8),
            ]
        ),
        Issue(
            id="ISSUE-002", 
            title="Falhas intermitentes na autenticação",
            description="""
            Usuários reportando logout inesperado e falhas de login.
            Problema parece ser relacionado a sessões e tokens.
            
            Contexto:
            - Acontece ~50 vezes por dia
            - Mais frequente após updates do sistema
            - Logs mostram tokens inválidos
            - Session timeout inconsistente
            - Alguns usuários afetados múltiplas vezes
            """,
            severity=ProblemSeverity.CRITICAL,
            status="Open",
            created_date=datetime(2024, 8, 20),
            component="Backend/Auth",
            labels=["security", "authentication", "session-management"],
            tasks=[
                Task("T006", "Investigar logs de autenticação", "Analisar padrões de falha", TaskStatus.COMPLETED, estimated_hours=6, actual_hours=8),
                Task("T007", "Revisar configuração de sessão", "Verificar timeouts e storage", TaskStatus.IN_PROGRESS, estimated_hours=4),
                Task("T008", "Implementar refresh token", "Melhorar gestão de tokens", TaskStatus.PENDING, estimated_hours=20),
                Task("T009", "Testes de stress auth", "Simular carga no sistema auth", TaskStatus.PENDING, estimated_hours=12),
            ]
        )
    ]
    
    # Inicializar agente sem GitHub
    analyzer = ProblemAnalyzerAgent("demo_structured")
    
    print("🔍 ANÁLISE ESTRUTURADA DE ISSUES")
    print("=" * 60)
    
    analyses = []
    
    # Analisar cada issue
    for issue in sample_issues:
        print(f"\n📋 Analisando Issue {issue.id}...")
        analysis = await analyzer.analyze_issue(issue)
        analyses.append(analysis)
        
        print(f"✅ Análise completada:")
        print(f"   📊 Débito Técnico: {analysis.technical_debt_score}/10")
        print(f"   🎯 Problemas identificados: {len(analysis.identified_problems)}")
        print(f"   💡 Recomendações: {len(analysis.recommendations)}")
        print(f"   🚀 Ações prioritárias: {len(analysis.priority_actions)}")
        print(f"   📈 Resumo: {analysis.analysis_summary[:100]}...")
    
    print(f"\n🗺️ GERANDO ROADMAP DE MELHORIAS")
    print("=" * 60)
    
    # Gerar roadmap estruturado
    roadmap = await analyzer.generate_improvement_roadmap(analyses)
    
    print(f"📋 Roadmap gerado:")
    print(f"   ⏱️  Duração total: {roadmap.total_estimated_duration}")
    print(f"   🎯 Fases: {len(roadmap.phases)}")
    print(f"   📊 Métricas de sucesso: {len(roadmap.success_metrics)}")
    print(f"   ⚠️  Riscos identificados: {len(roadmap.risks_and_mitigation)}")
    
    # Mostrar primeira fase
    if roadmap.phases:
        first_phase = roadmap.phases[0]
        print(f"\n   🚀 Primeira fase: {first_phase.phase_name}")
        print(f"      • Duração: {first_phase.duration}")
        print(f"      • Objetivo: {first_phase.objective}")
        print(f"      • Itens: {len(first_phase.items)}")
        
        # Mostrar primeiro item da primeira fase
        if first_phase.items:
            first_item = first_phase.items[0]
            print(f"      • Primeiro item: {first_item.title}")
            print(f"        - Prioridade: {first_item.priority.value}")
            print(f"        - Esforço: {first_item.effort.value}")
            print(f"        - Impacto: {first_item.expected_impact[:80]}...")
    
    print(f"\n🔄 IDENTIFICANDO PADRÕES")
    print("=" * 60)
    
    # Identificar padrões
    patterns = await analyzer.identify_patterns(sample_issues)
    
    print(f"🔍 Análise de padrões completada:")
    print(f"   📋 Padrões identificados: {len(patterns.identified_patterns)}")
    print(f"   💡 Recomendações sistêmicas: {len(patterns.systemic_recommendations)}")
    print(f"   🛡️  Estratégias de prevenção: {len(patterns.prevention_strategies)}")
    print(f"   ⚙️  Melhorias de processo: {len(patterns.process_improvements)}")
    
    # Mostrar primeiro padrão
    if patterns.identified_patterns:
        first_pattern = patterns.identified_patterns[0]
        print(f"\n   🔍 Primeiro padrão identificado:")
        print(f"      • Tipo: {first_pattern.pattern_type}")
        print(f"      • Frequência: {first_pattern.frequency}")
        print(f"      • Componentes afetados: {len(first_pattern.affected_components)}")
        print(f"      • Descrição: {first_pattern.description[:100]}...")
    
    # Mostrar primeira recomendação sistêmica
    if patterns.systemic_recommendations:
        first_rec = patterns.systemic_recommendations[0]
        print(f"\n   💡 Primeira recomendação sistêmica:")
        print(f"      • Título: {first_rec.title}")
        print(f"      • Esforço: {first_rec.effort_required.value}")
        print(f"      • Padrões alvo: {len(first_rec.target_patterns)}")
        print(f"      • Resultados esperados: {len(first_rec.expected_outcomes)}")
    
    print(f"\n✅ ANÁLISE ESTRUTURADA COMPLETADA!")
    print("=" * 60)
    print("Todos os dados estão estruturados e podem ser facilmente:")
    print("• Exportados para JSON/CSV")
    print("• Integrados com outras ferramentas")
    print("• Processados programaticamente")
    print("• Armazenados em banco de dados")
    print("• Utilizados para automações")


if __name__ == "__main__":
    asyncio.run(main())