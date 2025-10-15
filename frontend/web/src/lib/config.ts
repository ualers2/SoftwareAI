import { StartScreenPrompt } from "@openai/chatkit";

export const CHATKIT_API_URL =
  import.meta.env.VITE_CHATKIT_API_URL ?? "/chatkit";

/**
 * ChatKit still expects a domain key at runtime. Use any placeholder locally,
 * but register your production domain at
 * https://platform.openai.com/settings/organization/security/domain-allowlist
 * and deploy the real key.
 */
export const CHATKIT_API_DOMAIN_KEY =
  import.meta.env.VITE_CHATKIT_API_DOMAIN_KEY ?? "domain_pk_localhost_dev";

export const FACTS_API_URL = import.meta.env.VITE_FACTS_API_URL ?? "/facts";

export const THEME_STORAGE_KEY = "chatkit-boilerplate-theme";

export const GREETING = "Bem vindo Ao SoftwareAI";

export const STARTER_PROMPTS: StartScreenPrompt[] = [
  {
    label: "Quantos commits eu fiz esse mes?",
    prompt: "Quantos commits eu fiz esse mes?",
    icon: "circle-question",
  },
  {
    label: "Quantas tarefas os agentes fizeram hoje?",
    prompt: "Quantas tarefas os agentes fizeram hoje?",
    icon: "book-open",
  },
  {
    label: "O que o GCL fez na semana passada?",
    prompt: "O que o GCL fez na semana passada?",
    icon: "search",
  },
  {
    label: "Gere um grafico com 10 vendas e 30 ordens no app",
    prompt: "Gere um grafico com 10 vendas e 30 ordens no app",
    icon: "sparkle",
  },
];

export const PLACEHOLDER_INPUT = "Envie para a ia";
