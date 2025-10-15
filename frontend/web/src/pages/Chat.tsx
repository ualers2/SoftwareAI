import clsx from "clsx";
import { useState } from "react";

import { ChatKitPanel } from "@/components/ChatKitPanel";
import { ThemeToggle } from "@/components/ThemeToggle";
import { ColorScheme } from "@/hooks/useColorScheme";
import { useActions } from "@/hooks/useActions";
import { Aperture, Code, Sparkles } from "lucide-react";


const Chat = ({
    scheme,
    handleThemeChange,
}: {
    scheme: ColorScheme;
    handleThemeChange: (scheme: ColorScheme) => void;
}) => {

    const { refresh, performAction } = useActions(); 

    const containerClass = clsx(
        "min-h-screen bg-gradient-to-br transition-colors duration-300",
        scheme === "dark"
            ? "from-slate-900 via-slate-950 to-slate-850 text-slate-100"
            : "from-slate-100 via-white to-slate-200 text-slate-900"
    );

    return (
        <div className={containerClass}>
            <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col-reverse gap-10 px-6 pt-4 pb-10 md:py-10 lg:flex-row">
           
                
                <div 
                    className="relative w-full md:w-[100%] flex h-[90vh] items-stretch overflow-hidden rounded-3xl bg-white/80 shadow-[0_45px_90px_-45px_rgba(15,23,42,0.6)] ring-1 ring-slate-200/60 backdrop-blur md:h-[90vh] dark:bg-slate-900/70 dark:shadow-[0_45px_90px_-45px_rgba(15,23,42,0.85)] dark:ring-slate-800/60"
                >
                  <ChatKitPanel
                      theme={scheme}
                      onWidgetAction={performAction}
                      onResponseEnd={refresh}
                      onThemeRequest={handleThemeChange}
                  />
                </div>

            </div>
        </div>
    );
}
export default Chat;
