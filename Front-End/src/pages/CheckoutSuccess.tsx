// src/components/CheckoutSuccess.tsx
import React from "react";
import { Link } from "react-router-dom";

export default function CheckoutSuccess(): JSX.Element {
  const contentCreatorFeatures = [
    "Tudo do plano Startup +",
    "60 vídeos base por mês (Totalizando 90 por mês)",
    "Cortes em 2K (Quad HD)",
    "+ 1 projeto em simultâneo (Totalizando 2 em simultâneo)",
    "Remoção de marca d´água nos cortes",
  ];

  return (
    <div className="max-w-md mx-auto mt-20 bg-white rounded-2xl shadow-md p-6 text-center">
      <h2 className="text-3xl font-bold mb-4 text-green-600">Pagamento realizado com sucesso!</h2>
      <p className="text-gray-700 mb-6">
        Obrigado por assinar o plano <strong>Content Creator</strong>! Você já pode acessar seus conteúdos e ferramentas.
      </p>

      <div className="text-left bg-gray-50 p-4 rounded-lg mb-6">
        <h3 className="text-lg font-semibold mb-2">Recursos do Plano:</h3>
        <ul className="list-disc list-inside text-gray-700 space-y-1">
          {contentCreatorFeatures.map((feature, idx) => (
            <li key={idx}>{feature}</li>
          ))}
        </ul>
      </div>

      <Link
        to="/shortify"
        className="inline-block px-6 py-3 rounded-xl bg-gradient-to-r from-blue-700 to-blue-500 text-white font-semibold hover:from-blue-800 hover:to-blue-600 transition"
      >
        Ir para Dashboard
      </Link>
    </div>
  );
}
