/**
 * Minimal API client for the frontend. All functions are typed and return
 * parsed JSON. In a real app we would centralize error handling and token
 * refresh here.
 */

export type Contact = {
  id: string;
  email?: string | null;
  phone?: string | null;
  tags?: Record<string, unknown> | null;
  is_opt_in: boolean;
};

export type CampaignChannel = {
  channel_type: string;
  subject?: string | null;
  template?: string | null;
};

export type Campaign = {
  id: string;
  name: string;
  description?: string | null;
  status: string;
  scheduled_at?: string | null;
  sent_at?: string | null;
  channels: CampaignChannel[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const error = await res.text();
    throw new Error(error);
  }
  return res.json();
}

export async function getContacts(): Promise<Contact[]> {
  const res = await fetch(`${API_BASE}/contacts`);
  return handleResponse<Contact[]>(res);
}

export async function getContactById(id: string): Promise<Contact> {
  const res = await fetch(`${API_BASE}/contacts/${id}`);
  return handleResponse<Contact>(res);
}

export async function createContact(payload: Partial<Contact>): Promise<Contact> {
  const res = await fetch(`${API_BASE}/contacts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Contact>(res);
}

export async function getCampaigns(): Promise<Campaign[]> {
  const res = await fetch(`${API_BASE}/campaigns`);
  return handleResponse<Campaign[]>(res);
}

export async function createCampaign(payload: Partial<Campaign>): Promise<Campaign> {
  const res = await fetch(`${API_BASE}/campaigns`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Campaign>(res);
}
