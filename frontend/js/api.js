const API_BASE_URL = window.ENV?.API_URL || 'http://127.0.0.1:8000/api/v1';

const API = {
    async analyzeCode(code) {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        if (!response.ok) {
            throw new Error(`Analysis failed with status: ${response.status}`);
        }
        
        return await response.json();
    },
    
    async getResults() {
        const response = await fetch(`${API_BASE_URL}/results`);
        if (!response.ok) {
            throw new Error(`Failed to fetch results: ${response.status}`);
        }
        return await response.json();
    }
};

window.API = API;
