const BASE_URL = import.meta.env.VITE_GRADIO_BASE_URL || 'http://localhost:7862';

export async function fetchConfig() {
  const res = await fetch(`${BASE_URL}/config`);
  if (!res.ok) throw new Error('Failed to load Gradio config');
  return res.json();
}

export async function generateMusic({ description, duration, style }) {
  const config = await fetchConfig();
  const apiPrefix = config?.api_prefix || '';

  // Gradio v5 run endpoint expects a list in `data` and lowercase style values
  const payload = { data: [description, duration, String(style).toLowerCase()] };
  const res = await fetch(`${BASE_URL}${apiPrefix}/run/generate_music_simple`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Generation request failed');
  }
  const json = await res.json();
  const [fileData /*, statusText*/] = json?.data || [];

  // FileData may contain either `url` or `path`
  if (fileData?.url) {
    return { url: fileData.url, name: fileData.orig_name || 'audio' };
  }
  if (fileData?.path) {
    const url = `${BASE_URL}${apiPrefix}/file=${encodeURIComponent(fileData.path)}`;
    return { url, name: fileData.orig_name || fileData.path };
  }
  throw new Error('Unexpected audio response format');
}