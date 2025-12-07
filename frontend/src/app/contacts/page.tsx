"use client";

import { useEffect, useState } from "react";
import { Contact, createContact, getContacts } from "../../lib/api";

export default function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  useEffect(() => {
    getContacts().then(setContacts).catch(() => setContacts([]));
  }, []);

  const handleCreate = async () => {
    const created = await createContact({ email, phone, is_opt_in: true });
    setContacts((prev) => [...prev, created]);
    setEmail("");
    setPhone("");
  };

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-xl font-bold">Contactos</h1>
      <div className="space-y-2 max-w-md">
        <input className="border p-2 w-full" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Teléfono" value={phone} onChange={(e) => setPhone(e.target.value)} />
        <button className="bg-blue-600 text-white px-4 py-2" onClick={handleCreate}>
          Crear contacto
        </button>
      </div>
      <table className="min-w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">Email</th>
            <th className="p-2 text-left">Teléfono</th>
            <th className="p-2 text-left">Opt-in</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map((contact) => (
            <tr key={contact.id} className="border-t">
              <td className="p-2">{contact.email ?? "-"}</td>
              <td className="p-2">{contact.phone ?? "-"}</td>
              <td className="p-2">{contact.is_opt_in ? "Sí" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
