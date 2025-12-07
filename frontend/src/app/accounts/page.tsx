"use client";

import Link from "next/link";

export default function AccountsPage() {
  const oauthUrl = process.env.NEXT_PUBLIC_OAUTH_URL || "http://localhost:8000/api/v1/auth/oauth";

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-xl font-bold">Cuentas conectadas</h1>
      <p className="text-sm text-gray-600">
        En un despliegue real aquí listaríamos las cuentas conectadas desde la API y permitiríamos revocarlas.
      </p>
      <Link className="bg-green-600 text-white px-4 py-2 inline-block" href={oauthUrl}>
        Iniciar flujo OAuth
      </Link>
    </main>
  );
}
