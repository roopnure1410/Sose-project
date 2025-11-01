const GRADIO_BASE_URL = 'http://localhost:7862';

class GradioClientV5 {
  constructor(baseUrl = GRADIO_BASE_URL) {
    this.baseUrl = baseUrl;
    this.config = null;
  }

  async getConfig() {
    if (!this.config) {
      const response = await fetch(`${this.baseUrl}/config`);
      if (!response.ok) {
        throw new Error(`Failed to fetch Gradio config: ${response.status}`);
      }
      this.config = await response.json();
    }
    return this.config;
  }

  async run(apiName, inputs) {
    const config = await this.getConfig();
    const apiPrefix = config.api_prefix || '';

    const response = await fetch(`${this.baseUrl}${apiPrefix}/run/${apiName}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data: inputs }),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`HTTP ${response.status}: ${text}`);
    }
    return await response.json();
  }

  async generateMusic(description, duration = 5, style = 'classical') {
    const payload = [description, duration, style];
    const result = await this.run('generate_music_simple', payload);

    const data = result?.data || [];
    const fileData = data[0];
    const statusText = data[1];

    let trackUrl = null;
    if (fileData) {
      if (fileData.url) {
        trackUrl = fileData.url;
      } else if (fileData.path) {
        const apiPrefix = (this.config?.api_prefix) || '';
        const encodedPath = encodeURIComponent(fileData.path);
        trackUrl = `${this.baseUrl}${apiPrefix}/file=${encodedPath}`;
      }
    }

    return { tracks: trackUrl ? [trackUrl] : [], status: statusText };
  }
}

export default new GradioClientV5();