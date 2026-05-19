document.addEventListener('DOMContentLoaded', () => {
    
    // File upload handling
    const fileUpload = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const codeInput = document.getElementById('code-input');
    
    if (fileUpload && codeInput) {
        fileUpload.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                fileNameDisplay.textContent = file.name;
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    codeInput.value = e.target.result;
                };
                reader.readAsText(file);
            } else {
                fileNameDisplay.textContent = 'No file chosen';
            }
        });
    }

    // Analyze form submission
    const analyzeForm = document.getElementById('analyze-form');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btnText = document.getElementById('btn-text');
            const spinner = document.getElementById('loading-spinner');
            const analyzeBtn = document.getElementById('analyze-btn');
            const errorMsg = document.getElementById('error-message');
            
            // UI state: loading
            analyzeBtn.disabled = true;
            btnText.textContent = 'Analyzing...';
            spinner.classList.remove('hidden');
            errorMsg.classList.add('hidden');
            
            const code = codeInput.value;
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: code, user_id: 1 }) // Backend expects CodeRequest
                });
                
                if (!response.ok) {
                    throw new Error(`Analysis failed with status: ${response.status}`);
                }
                
                // Store success and redirect
                window.location.href = '/results_page';
                
            } catch (error) {
                console.error("Error during analysis:", error);
                errorMsg.textContent = "Error: " + error.message;
                errorMsg.classList.remove('hidden');
                
                // Reset UI state
                analyzeBtn.disabled = false;
                btnText.textContent = 'Analyze Code';
                spinner.classList.add('hidden');
            }
        });
    }
});

// Load Results Page
async function loadResults() {
    const resultsContainer = document.getElementById('results-content');
    const loadingState = document.getElementById('loading-results');
    const errorMsg = document.getElementById('error-message');
    const noIssues = document.getElementById('no-issues');
    const issuesContainer = document.getElementById('issues-container');
    
    if (!resultsContainer) return; // Not on results page
    
    try {
        const response = await fetch('/results');
        if (!response.ok) {
            throw new Error(`Failed to fetch results: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading
        loadingState.classList.add('hidden');
        resultsContainer.classList.remove('hidden');
        
        const issues = data.issues || [];
        
        // Calculate counts and score
        let highCount = 0;
        let mediumCount = 0;
        let lowCount = 0;
        
        issuesContainer.innerHTML = '';
        
        if (issues.length === 0) {
            noIssues.classList.remove('hidden');
            document.getElementById('score-value').textContent = "100";
            return;
        }
        
        issues.forEach(issue => {
            const severity = (issue.severity || 'Medium').toLowerCase();
            if (severity === 'high' || severity === 'critical') highCount++;
            else if (severity === 'low' || severity === 'info') lowCount++;
            else mediumCount++;
            
            const badgeClass = severity === 'high' || severity === 'critical' ? 'badge-high' : 
                              (severity === 'low' || severity === 'info' ? 'badge-low' : 'badge-medium');
            
            const issueHTML = `
                <div class="issue-item severity-${severity}">
                    <div class="issue-header">
                        <span class="issue-type">${issue.type || 'Issue'}</span>
                        <div class="issue-meta">
                            <span class="badge ${badgeClass}">${issue.severity || 'Medium'}</span>
                        </div>
                    </div>
                    <p class="issue-desc">${issue.description || 'No description available.'}</p>
                    ${issue.line_number ? `<div class="issue-line">Line: ${issue.line_number}</div>` : ''}
                </div>
            `;
            issuesContainer.innerHTML += issueHTML;
        });
        
        // Update stats
        document.getElementById('high-count').textContent = highCount;
        document.getElementById('medium-count').textContent = mediumCount;
        document.getElementById('low-count').textContent = lowCount;
        
        // Simple score calculation based on issues
        const deduction = (highCount * 10) + (mediumCount * 5) + (lowCount * 2);
        const score = Math.max(0, 100 - deduction);
        
        const scoreEl = document.getElementById('score-value');
        scoreEl.textContent = score;
        
        if (score < 50) {
            scoreEl.style.color = 'var(--danger)';
        } else if (score < 80) {
            scoreEl.style.color = 'var(--warning)';
        }
        
    } catch (error) {
        console.error("Error loading results:", error);
        loadingState.classList.add('hidden');
        errorMsg.textContent = "Failed to load results. Please try analyzing code again.";
        errorMsg.classList.remove('hidden');
    }
}
