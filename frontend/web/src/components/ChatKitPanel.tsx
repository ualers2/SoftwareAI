import { useRef } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import {
  CHATKIT_API_URL,
  CHATKIT_API_DOMAIN_KEY,
  STARTER_PROMPTS,
  PLACEHOLDER_INPUT,
  GREETING,
} from "../lib/config";
import type { Actions } from "../hooks/useActions";
import type { ColorScheme } from "../hooks/useColorScheme";


// Configurações padrão para attachments — ajuste conforme necessário
const DEFAULT_MAX_SIZE = 100 * 1024 * 1024; // 100MB
const DEFAULT_MAX_COUNT = 10;
const DEFAULT_ACCEPT = {
"image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
"video/*": [".mp4", ".mov", ".webm"],
"application/pdf": [".pdf"],
"text/plain": [".txt"],
"application/zip": [".zip"],
};


type ChatKitPanelProps = {
  theme: ColorScheme;
  onWidgetAction: (action: Actions) => Promise<void>;
  onResponseEnd: () => void;
  onThemeRequest: (scheme: ColorScheme) => void;
};

export function ChatKitPanel({
  theme,
  onWidgetAction,
  onResponseEnd,
  onThemeRequest,
}: ChatKitPanelProps) {
  const processedFacts = useRef(new Set<string>());
  function validateAttachments(files?: FileList | null) {
    const errors: string[] = [];
    if (!files || files.length === 0) return { ok: true, errors };


    if (files.length > DEFAULT_MAX_COUNT) {
    errors.push(`Máximo de anexos permitido: ${DEFAULT_MAX_COUNT}`);
    }


    for (let i = 0; i < files.length; i++) {
    const f = files[i];
    if (f.size > DEFAULT_MAX_SIZE) {
    errors.push(`${f.name}: excede o tamanho máximo de ${Math.round(
    DEFAULT_MAX_SIZE / (1024 * 1024)
    )}MB`);
    }
    // validação de tipo com base na extensão (aceita ou não)
    // nota: checagem de MIME nem sempre é confiável do lado do cliente
    const ext = (f.name.match(/\.[0-9a-z]+$/i)?.[0] || "").toLowerCase();
    const allowedExts = Object.values(DEFAULT_ACCEPT).flat();
    if (allowedExts.length > 0 && !allowedExts.includes(ext)) {
    errors.push(`${f.name}: tipo não permitido`);
    }
    }


    return { ok: errors.length === 0, errors };
  }
  const chatkit = useChatKit({
    api: { 
      url: CHATKIT_API_URL, 
      domainKey: CHATKIT_API_DOMAIN_KEY,
      // uploadStrategy: {
      //   type: "direct", // ou "hosted" dependendo do seu fluxo
      //   uploadUrl: "https://meu-backend.example.com/chatkit/upload",
      // },
    },
    theme: {
      colorScheme: theme,
      color: {
        grayscale: {
          hue: 220,
          tint: 6,
          shade: theme === "dark" ? -1 : -4,
        },
        accent: {
          primary: theme === "dark" ? "#f1f5f9" : "#0f172a",
          level: 1,
        },
      },
      radius: "round",
    },
    startScreen: {
      greeting: GREETING,
      prompts: STARTER_PROMPTS,
    },

    composer: {
      placeholder: PLACEHOLDER_INPUT,
      // attachments: {
      //   enabled: true,
      //   maxSize: DEFAULT_MAX_SIZE,
      //   maxCount: DEFAULT_MAX_COUNT,
      //   accept: DEFAULT_ACCEPT,
      // },
      tools: [
        {
          id: 'chart_generator',
          label: 'Gere Graficos',
          shortLabel: 'Graficos',
          placeholderOverride: 'Crie Graficos Com IA',
          icon: 'chart',
          pinned: true,
        }
      ],
      models: [
        {
          id: 'Chat',
          label: 'Chat',
          description: 'Apenas Chat'
        },
        {
          id: 'documentation',
          label: 'Documentation',
          description: 'Documentar apis e codigos'
        }
        // ...and 2 more models
      ],
    },
    threadItemActions: {
      feedback: false,
    },

    onClientTool: async (invocation) => {
      console.log(`onClientTool invocation ${invocation}`);
      if (invocation.name === "chart_generator") {
        const id = String(invocation.params.fact_id ?? "");
        console.log(`onClientTool chart_generator ${id}`);
        const requested = "light" 
        console.debug("[ChatKitPanel] switch_theme teste", requested);
        onThemeRequest(requested);
        return { success: false };
      }  
      if (invocation.name === "switch_theme") {
        const requested = invocation.params.theme;
        if (requested === "light" || requested === "dark") {
          if (import.meta.env.DEV) {
            console.debug("[ChatKitPanel] switch_theme", requested);
          }
          onThemeRequest(requested);
          return { success: true };
        }
        return { success: false };
      }

      if (invocation.name === "record_fact") {
        const id = String(invocation.params.fact_id ?? "");
        const text = String(invocation.params.fact_text ?? "");
        if (!id || processedFacts.current.has(id)) {
          return { success: true };
        }
        processedFacts.current.add(id);
        void onWidgetAction({
          type: "save",
          factId: id,
          factText: text.replace(/\s+/g, " ").trim(),
        });
        return { success: true };
      }

      return { success: false };
    },
    onResponseEnd: () => {
      onResponseEnd();
    },
    onThreadChange: () => {
      processedFacts.current.clear();
    },
    onError: ({ error }) => {
      // ChatKit handles displaying the error to the user
      console.error("ChatKit error", error);
    },
  });
  console.log(chatkit.control);

  return (
    <div className="relative h-full w-full overflow-hidden border border-slate-200/60 bg-white shadow-card dark:border-slate-800/70 dark:bg-slate-900">
      <ChatKit control={chatkit.control} className="block h-full w-full" />
    </div>
  );
}
