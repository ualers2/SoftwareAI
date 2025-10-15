from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import re

# Configuração de logging
diretorio_script = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
os.makedirs(os.path.join(diretorio_script, 'Logs'), exist_ok=True)
file_handler = logging.FileHandler(os.path.join(diretorio_script, 'Logs', 'job_automation.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))

class AutomatedJobSearcher:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"
        self.email_config = {
            'smtp_user': os.getenv("SMTP_USER"),
            'smtp_password': os.getenv("SMTP_PASSWORD"),
            'smtp_host': os.getenv("SMTP_HOST"),
            'smtp_port': int(os.getenv("SMTP_PORT", 587)),
            'use_tls': os.getenv("SMTP_USE_TLS", "true").lower() == "true",
            'recipient_email': os.getenv("RECIPIENT_EMAIL")  # Email para receber relatórios
        }
        self.reports_dir = os.path.join(diretorio_script, 'Reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def get_current_resume(self):
        """Obtém o currículo atual e extrai tecnologias/frameworks"""
        try:
            # Busca por arquivo de currículo no diretório
            resume_files = [f for f in os.listdir(diretorio_script) 
                            if f.lower().endswith(('.txt', '.md', '.pdf', '.docx')) 
                            and 'curriculo' in f.lower() or 'resume' in f.lower()]
            
            if resume_files:
                resume_path = os.path.join(diretorio_script, resume_files[0])
                if resume_path.endswith('.txt') or resume_path.endswith('.md'):
                    with open(resume_path, 'r', encoding='utf-8') as f:
                        resume_content = f.read()
                        logger.info(f"resume_content {resume_content}")
                else:
                    # Para arquivos PDF/DOCX, usar placeholder ou implementar extração
                    resume_content = "Currículo com experiência em Python, JavaScript, React, Django, FastAPI"
            else:
                # Currículo padrão se não encontrar arquivo
                resume_content = """
                Desenvolvedor Full Stack com experiência em:
                - Python (Django, FastAPI, Flask)
                - JavaScript (React, Node.js, Vue.js)
                - Bancos de dados (PostgreSQL, MongoDB, MySQL)
                - DevOps (Docker, AWS, Git)
                - Machine Learning (TensorFlow, scikit-learn)
                """
            
            return self.extract_technologies_from_resume(resume_content)
            
        except Exception as e:
            logger.error(f"Erro ao obter currículo: {str(e)}")
            return {
                'languages': ['Python', 'JavaScript'],
                'frameworks': ['Django', 'React', 'FastAPI'],
                'databases': ['PostgreSQL', 'MongoDB'],
                'tools': ['Docker', 'Git', 'AWS']
            }
    
    def extract_technologies_from_resume(self, resume_content):
        """Extrai tecnologias do currículo usando GPT"""
        try:
            response = self.client.responses.create(
                model=self.model,
                input=f"""
                Analise este currículo e extraia todas as tecnologias, linguagens de programação, 
                frameworks e ferramentas mencionadas. Organize em categorias.
                
                Retorne em formato JSON assim:
                {{
                    "languages": ["Python", "JavaScript", "Java"],
                    "frameworks": ["Django", "React", "Angular"],
                    "databases": ["PostgreSQL", "MongoDB"],
                    "tools": ["Docker", "AWS", "Git"],
                    "other": ["outras tecnologias"]
                }}
                
                Currículo:
                {resume_content}
                """,
                
            )
            
            # Extrair JSON da resposta
            json_match = re.search(r'\{.*\}', response.output_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise Exception("Não foi possível extrair JSON da resposta")
                
        except Exception as e:
            logger.error(f"Erro na extração de tecnologias: {str(e)}")
            return self.get_default_technologies()
    
    def get_default_technologies(self):
        """Tecnologias padrão caso falhe a extração"""
        return {
            'languages': ['Python', 'JavaScript', 'TypeScript'],
            'frameworks': ['Django', 'React', 'FastAPI', 'Node.js'],
            'databases': ['PostgreSQL', 'MongoDB', 'MySQL'],
            'tools': ['Docker', 'Git', 'AWS'],
            'other': ['REST API', 'GraphQL']
        }
    
    def search_jobs_by_technologies(self, technologies):
        """Busca vagas baseadas nas tecnologias do currículo"""
        all_jobs = []
        
        # Criar queries de busca baseadas nas tecnologias
        tech_combinations = [
            f"{tech} desenvolvedor Brasil remoto" for tech in technologies['languages'][:3]
        ] + [
            f"{framework} developer vagas freelance" for framework in technologies['frameworks'][:3]
        ] + [
            f"full stack {' '.join(technologies['languages'][:2])} vagas"
        ]
        
        for query in tech_combinations:
            try:
                logger.info(f"Buscando vagas para: {query}")
                
                response = self.client.responses.create(
                    model=self.model,
                    input=f"""
                    Você é um especialista em busca de vagas de emprego e freelances.
                    Busque vagas e projetos freelance para: {query}
                    
                    Para CADA vaga/freela encontrada, formate EXATAMENTE assim:
                    
                    ## TÍTULO_DA_VAGA
                    - **URL**: link_da_vaga_ou_N/A
                    - **Empresa/Cliente**: nome_da_empresa_ou_cliente
                    - **Ganhos**: valor_salario_ou_projeto
                    - **Tecnologias**: lista_de_tecnologias_requeridas
                    - **Tempo**: tempo_dedicacao_ou_duracao_projeto
                    - **Tipo**: CLT/PJ/Freelance
                    - **Local**: cidade_ou_remoto
                    - **Descrição**: resumo_breve_da_vaga
                    
                    ---
                    
                    Encontre pelo menos 10-20 oportunidades relevantes. Seja específico e detalhado.
                    """,
                    tools=[{
                        "type": "web_search_preview",
                        "search_context_size": "low",
                    }],
                )
                
                all_jobs.append({
                    'query': query,
                    'results': response.output_text
                })
                
                # Pequena pausa entre buscas
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erro na busca para {query}: {str(e)}")
                continue
        
        return all_jobs
    
    def generate_report(self, technologies, jobs_data, report_type):
        """Gera relatório consolidado em Markdown"""
        try:
            # Combinar todos os resultados
            combined_results = "\n\n".join([job['results'] for job in jobs_data])
            
            if report_type == "vagas":
                title = "# 📊 Relatório de Vagas CLT/PJ"
                section_title = "## 💼 Vagas CLT/PJ"
                prompt_sections = f"""
                Crie um relatório profissional em Markdown consolidando estas informações sobre vagas CLT/PJ.
                
                ESTRUTURA OBRIGATÓRIA:
                
                # 📊 Relatório de Vagas CLT/PJ
                **Data**: {datetime.now().strftime('%d/%m/%Y')}
                **Tecnologias do Perfil**: {', '.join(technologies['languages'] + technologies['frameworks'])}
                
                ## 🎯 Resumo Executivo
                [Resumo das oportunidades CLT/PJ, tendências de mercado, faixa salarial]
                
                ## 💼 Vagas CLT/PJ
                [Listar vagas de emprego encontradas com todos os metadados]
                
                ## 📈 Análise de Mercado para Vagas
                [Análise das tecnologias mais demandadas, empresas que mais contratam]
                
                ## 💡 Recomendações
                [Sugestões para o profissional em relação a vagas de emprego]
                
                ---
                
                DADOS COLETADOS:
                {combined_results}
                
                IMPORTANTE: Mantenha TODOS os metadados (URL, ganhos, tecnologias, tempo, tipo, etc.) 
                organizados de forma clara e profissional.
                """
            elif report_type == "freelances":
                title = "# 🚀 Relatório de Projetos Freelance"
                section_title = "## 🚀 Projetos Freelance"
                prompt_sections = f"""
                Crie um relatório profissional em Markdown consolidando estas informações sobre projetos freelance.
                
                ESTRUTURA OBRIGATÓRIA:
                
                # 🚀 Relatório de Projetos Freelance
                **Data**: {datetime.now().strftime('%d/%m/%Y')}
                **Tecnologias do Perfil**: {', '.join(technologies['languages'] + technologies['frameworks'])}
                
                ## 🎯 Resumo Executivo
                [Resumo das oportunidades freelance, tendências de projetos, faixas de valor]
                
                ## 🚀 Projetos Freelance
                [Listar projetos freelance encontrados com todos os metadados]
                
                ## 📈 Análise de Mercado para Freelances
                [Análise das tecnologias mais demandadas em projetos, tipos de clientes]
                
                ## 💡 Recomendações
                [Sugestões para o profissional em relação a projetos freelance]
                
                ---
                
                DADOS COLETADOS:
                {combined_results}
                
                IMPORTANTE: Mantenha TODOS os metadados (URL, ganhos, tecnologias, tempo, tipo, etc.) 
                organizados de forma clara e profissional.
                """
            else:
                raise ValueError("Tipo de relatório inválido. Use 'vagas' ou 'freelances'.")
            
            response = self.client.responses.create(
                model=self.model,
                input=prompt_sections.format(
                    datetime=datetime,
                    technologies=technologies,
                    combined_results=combined_results
                )
            )
            
            return response.output_text
            
        except Exception as e:
            logger.error(f"Erro na geração do relatório de {report_type}: {str(e)}")
            return self.generate_fallback_report(technologies, jobs_data)
    
    def generate_fallback_report(self, technologies, jobs_data):
        """Gera relatório básico em caso de erro"""
        report = f"""# 📊 Relatório de Oportunidades Profissionais
**Data**: {datetime.now().strftime('%d/%m/%Y')}
**Tecnologias do Perfil**: {', '.join(technologies['languages'] + technologies['frameworks'])}

## 🎯 Dados Coletados

"""
        for job in jobs_data:
            report += f"### Busca: {job['query']}\n"
            report += f"{job['results']}\n\n---\n\n"
        
        return report
    
    def save_report(self, report_content, report_type):
        """Salva o relatório em arquivo .md"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"relatorio_{report_type}_{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"Relatório de {report_type} salvo em: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Erro ao salvar relatório de {report_type}: {str(e)}")
            return None
    
    def send_email_with_attachment(self, subject, body, attachment_paths):
        """Envia email com múltiplos anexos usando a configuração existente"""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"Job Automation <{self.email_config['smtp_user']}>"
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = subject
            
            # Corpo do email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Anexar arquivos
            for attachment_path in attachment_paths:
                if attachment_path and os.path.exists(attachment_path):
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
            
            # Enviar email
            server = smtplib.SMTP(self.email_config['smtp_host'], self.email_config['smtp_port'])
            
            if self.email_config['use_tls']:
                server.starttls()
            
            server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            logger.info("Email enviado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return False
    
    def run_daily_search(self):
        """Executa a busca diária completa"""
        logger.info("=== INICIANDO BUSCA DIÁRIA DE OPORTUNIDADES ===")
        
        try:
            # 1. Obter currículo e tecnologias
            logger.info("1. Obtendo tecnologias do currículo...")
            technologies = self.get_current_resume()
            logger.info(f"    Tecnologias encontradas: {technologies['languages']}")
            
            # 2. Buscar vagas baseadas nas tecnologias
            logger.info("2. Buscando vagas em plataformas específicas...")
            jobs_data = self.search_jobs_by_technologies(technologies)
            logger.info(f"    Realizadas {len(jobs_data)} buscas em diferentes plataformas")
            
            # Separar os dados em CLT/PJ e Freelance
            vagas_data = [j for j in jobs_data if 'CLT/PJ' in j['results'] or 'vagas' in j['query']]
            freelances_data = [j for j in jobs_data if 'Freelance' in j['results'] or 'freelance' in j['query']]
            
            # 3. Gerar relatórios separados
            logger.info("3. Gerando relatórios separados...")
            report_vagas = self.generate_report(technologies, vagas_data, "vagas")
            report_freelances = self.generate_report(technologies, freelances_data, "freelances")
            
            # 4. Adicionar instruções de busca manual
            report_vagas = self.add_manual_search_instructions(report_vagas, technologies)
            report_freelances = self.add_manual_search_instructions(report_freelances, technologies)
            
            # 5. Salvar relatórios
            logger.info("4. Salvando relatórios...")
            report_vagas_path = self.save_report(report_vagas, "vagas")
            report_freelances_path = self.save_report(report_freelances, "freelances")
            
            # 6. Enviar por email
            logger.info("5. Enviando email com anexos...")
            attachment_paths = []
            if report_vagas_path:
                attachment_paths.append(report_vagas_path)
            if report_freelances_path:
                attachment_paths.append(report_freelances_path)
            
            if attachment_paths:
                email_subject = f"📊 Relatório de Oportunidades - {datetime.now().strftime('%d/%m/%Y')}"
                email_body = f"""
Olá!

Segue o relatório diário de oportunidades profissionais, agora separado em duas categorias para melhor organização:
- **Relatório de Vagas CLT/PJ**
- **Relatório de Projetos Freelance**

🎯 Tecnologias pesquisadas: {', '.join(technologies['languages'][:3] + technologies['frameworks'][:2])}
📅 Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

💡 DICA: Configure alertas de vaga diretamente nas plataformas mencionadas!

Atenciosamente,
Sistema de Busca Automatizada
"""
                success = self.send_email_with_attachment(email_subject, email_body, attachment_paths)
                if success:
                    logger.info("    Email enviado com sucesso!")
                else:
                    logger.error("    Falha no envio do email")
            else:
                logger.error("    Nenhum relatório foi gerado para envio.")
            
            logger.info("=== BUSCA DIÁRIA CONCLUÍDA COM SUCESSO ===")
            
        except Exception as e:
            logger.error(f"Erro na busca diária: {str(e)}")
            # Enviar email de erro
            error_subject = "⚠️ Erro na Busca Diária de Vagas"
            error_body = f"""
Ocorreu um erro na busca diária de vagas:

ERRO: {str(e)}
TIMESTAMP: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

O sistema tentará executar novamente no próximo horário agendado.

Verifique os logs para mais detalhes.
"""
            self.send_email_with_attachment(error_subject, error_body, [])

    def add_manual_search_instructions(self, report, technologies):
        """Adiciona instruções detalhadas para busca manual"""
        tech_list = ', '.join(technologies['languages'][:3])
        
        instructions = f"""

## 🔍 Guia de Busca Manual nas Plataformas

### 🎯 Palavras-chave Recomendadas
**Principais**: {tech_list}
**Frameworks**: {', '.join(technologies['frameworks'][:3])}
**Termos complementares**: desenvolvedor, programador, full stack, backend, frontend

### 🌐 Links Diretos das Plataformas

#### 💼 Vagas CLT/PJ
- **Programathor**: https://programathor.com.br/jobs
- **InfoJobs**: https://www.infojobs.com.br/
- **Vagas.com**: https://www.vagas.com.br/
- **LinkedIn Jobs**: https://www.linkedin.com/jobs/
- **Indeed**: https://br.indeed.com/

#### 🚀 Freelances/Projetos
- **99Freelas**: https://www.99freelas.com.br/
- **Workana**: https://www.workana.com/pt/
- **Freelancer**: https://www.freelancer.com/
- **GetNinjas**: https://www.getninjas.com.br/

#### 🏠 Trabalho Remoto
- **Remotar**: https://remotar.com.br/
- **Remote.co**: https://remote.co/
- **We Work Remotely**: https://weworkremotely.com/

### 📱 Como Configurar Alertas

#### LinkedIn
1. Acesse LinkedIn Jobs
2. Busque por "{tech_list.split(', ')[0]} desenvolvedor"
3. Clique em "Criar alerta" 
4. Configure frequência diária

#### Google Jobs
1. Google: "vagas {tech_list.split(', ')[0]} desenvolvedor"
2. Clique em "Criar alerta" nos resultados
3. Receba notificações por email

### 💡 Dicas de Busca Eficaz
- Use aspas para termos exatos: "{tech_list.split(', ')[0]} developer"
- Combine tecnologias: "{tech_list.split(', ')[0]} + {tech_list.split(', ')[1] if len(tech_list.split(', ')) > 1 else 'JavaScript'}"
- Filtre por data: últimas 24h/semana
- Configure filtros de localização e salário

"""
        
        return report + instructions

def setup_scheduler():
    """Configura o agendamento das buscas"""
    searcher = AutomatedJobSearcher()
    
    # Agendar para horários de trabalho (9h, 13h, 17h)
    schedule.every().day.at("09:00").do(searcher.run_daily_search)
    schedule.every().day.at("13:00").do(searcher.run_daily_search) 
    schedule.every().day.at("17:00").do(searcher.run_daily_search)
    
    logger.info("Scheduler configurado para: 09:00, 13:00, 17:00")
    
    return searcher

def main(process):
    """Função principal - pode ser executada manualmente ou via scheduler"""
    import sys
    
    if process == 'test':
        # Execução de teste
        logger.info("=== MODO TESTE ===")
        searcher = AutomatedJobSearcher()
        searcher.run_daily_search()
    elif process == 'scheduler':
        # Modo scheduler contínuo
        logger.info("=== INICIANDO SCHEDULER ===")
        setup_scheduler()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    else:
        # Execução única
        logger.info("=== EXECUÇÃO ÚNICA ===")
        searcher = AutomatedJobSearcher()
        searcher.run_daily_search()

if __name__ == "__main__":
    main('test')