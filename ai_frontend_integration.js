/**
 * AI Frontend Integration for Vastu Vision
 * Handles all AI-powered features: Blueprint generation, Layout suggestions, Energy heatmaps
 */

class VastuAIIntegration {
    constructor() {
        this.aiServices = {
            blueprint: 'http://localhost:5003',
            layout: 'http://localhost:5004',
            heatmap: 'http://localhost:5005'
        };
        this.checkServiceStatus();
    }

    /**
     * Check which AI services are available
     */
    async checkServiceStatus() {
        try {
            const [blueprintStatus, layoutStatus, heatmapStatus] = await Promise.all([
                fetch(`${this.aiServices.blueprint}/health`).catch(() => null),
                fetch(`${this.aiServices.layout}/health`).catch(() => null),
                fetch(`${this.aiServices.heatmap}/health`).catch(() => null)
            ]);

            this.servicesAvailable = {
                blueprint: blueprintStatus && blueprintStatus.ok,
                layout: layoutStatus && layoutStatus.ok,
                heatmap: heatmapStatus && heatmapStatus.ok
            };

            console.log('🤖 AI Services Status:', this.servicesAvailable);
        } catch (error) {
            console.warn('⚠️ Could not check AI service status:', error);
            // Default to true for graceful degradation
            this.servicesAvailable = {
                blueprint: true,  // Will fallback to procedural
                layout: true,     // Will use rule-based
                heatmap: true      // Works independently
            };
        }
    }

    /**
     * Generate AI-powered blueprint
     */
    async generateAIBlueprint(spaceData) {
        try {
            // Try AI service first
            const response = await fetch(`${this.aiServices.blueprint}/generate_ai_blueprint`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData),
                timeout: 5000
            }).catch(() => null);

            if (response && response.ok) {
                const result = await response.json();
                if (result.success && result.image) {
                    return {
                        success: true,
                        image: result.image,
                        prompt: result.prompt_used,
                        service: result.service,
                        type: 'ai_generated'
                    };
                }
            }
            
            // Always fallback to procedural - never throw error
            console.log('ℹ️ AI service unavailable, using procedural generation...');
            return this.generateProceduralBlueprint(spaceData);
        } catch (error) {
            console.warn('AI Blueprint error, using fallback:', error);
            // Always fallback to procedural
            return this.generateProceduralBlueprint(spaceData);
        }
    }

    /**
     * Fallback to procedural blueprint generation
     */
    async generateProceduralBlueprint(spaceData) {
        try {
            // Try professional blueprint generator first (better quality)
            const professionalResponse = await fetch('http://localhost:5006/generate_professional_blueprint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData),
                timeout: 15000
            }).catch(() => null);

            if (professionalResponse && professionalResponse.ok) {
                const professionalResult = await professionalResponse.json();
                if (professionalResult.success && professionalResult.image) {
                    return {
                        success: true,
                        image: professionalResult.image,
                        type: 'professional_detailed',
                        fallback: false
                    };
                }
            }

            // Fallback to old blueprint generator
            const response = await fetch('http://localhost:5002/generate_blueprints', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData)
            });

            const result = await response.json();
            if (result.success && result.blueprints && result.blueprints.length > 0) {
                return {
                    success: true,
                    image: result.blueprints[0].image, // First blueprint
                    type: 'procedural',
                    fallback: true
                };
            }
            throw new Error('Procedural generation also failed');
        } catch (error) {
            throw new Error(`Blueprint generation failed: ${error.message}`);
        }
    }

    /**
     * Generate 3D visualization
     */
    async generate3DVisualization(spaceData) {
        try {
            const response = await fetch('http://localhost:5007/generate_3d_visualization', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData),
                timeout: 15000
            }).catch(() => null);

            if (response && response.ok) {
                const result = await response.json();
                if (result.success && result.image) {
                    return {
                        success: true,
                        image: result.image,
                        type: '3d_visualization'
                    };
                }
            }
            
            throw new Error('3D visualization service unavailable');
        } catch (error) {
            throw new Error(`3D visualization failed: ${error.message}`);
        }
    }

    /**
     * Get AI layout suggestions
     */
    async getLayoutSuggestions(spaceData) {
        if (!this.servicesAvailable.layout) {
            return this.getRuleBasedSuggestions(spaceData);
        }

        try {
            const response = await fetch(`${this.aiServices.layout}/suggest_layout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData)
            });

            const result = await response.json();

            if (result.success) {
                return {
                    success: true,
                    suggestions: result.suggestions,
                    ai_enhanced: result.ai_enhanced,
                    method: result.method
                };
            }
        } catch (error) {
            console.error('AI Layout suggestions failed:', error);
            return this.getRuleBasedSuggestions(spaceData);
        }
    }

    /**
     * Fallback to rule-based suggestions
     */
    async getRuleBasedSuggestions(spaceData) {
        // This uses the AI service's fallback logic
        return {
            success: true,
            suggestions: [],
            method: 'rule_based',
            message: 'Using rule-based Vastu suggestions'
        };
    }

    /**
     * Generate energy balance heatmap
     */
    async generateEnergyHeatmap(spaceData, element = 'all') {
        try {
            const response = await fetch(`${this.aiServices.heatmap}/generate_heatmap`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ...spaceData,
                    element: element
                }),
                timeout: 10000
            }).catch(() => null);

            if (response && response.ok) {
                const result = await response.json();
                if (result.success && result.heatmap) {
                    return {
                        success: true,
                        heatmap: result.heatmap,
                        zone_energy: result.zone_energy,
                        element_balance: result.element_balance,
                        element: result.element
                    };
                }
            }
            
            // Generate a simple fallback visualization
            console.log('ℹ️ Heatmap service unavailable, generating fallback...');
            return this.generateFallbackHeatmap(spaceData, element);
        } catch (error) {
            console.warn('Heatmap generation error, using fallback:', error);
            return this.generateFallbackHeatmap(spaceData, element);
        }
    }

    /**
     * Generate fallback heatmap visualization
     */
    generateFallbackHeatmap(spaceData, element) {
        // Return a simple visualization message
        return {
            success: true,
            heatmap: null, // Will show message instead
            zone_energy: {},
            element_balance: {},
            element: element,
            fallback: true,
            message: 'Heatmap service is starting. Please refresh the page in a moment.'
        };
    }

    /**
     * Calculate energy balance without image
     */
    async calculateEnergyBalance(spaceData) {
        if (!this.servicesAvailable.heatmap) {
            throw new Error('Energy Heatmap service not available');
        }

        try {
            const response = await fetch(`${this.aiServices.heatmap}/calculate_energy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData)
            });

            const result = await response.json();

            if (result.success) {
                return {
                    success: true,
                    zone_energy: result.zone_energy,
                    element_balance: result.element_balance
                };
            } else {
                throw new Error(result.error || 'Energy calculation failed');
            }
        } catch (error) {
            throw new Error(`Energy calculation failed: ${error.message}`);
        }
    }

    /**
     * Get Vastu rules for a specific room
     */
    async getVastuRules(roomType) {
        try {
            const response = await fetch(`${this.aiServices.layout}/vastu_rules/${encodeURIComponent(roomType)}`);
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Failed to get Vastu rules:', error);
            return null;
        }
    }

    /**
     * Generate 3D visualization
     */
    async generate3DVisualization(spaceData) {
        try {
            const response = await fetch(`${this.aiServices.heatmap.replace('5005', '5007')}/generate_3d_visualization`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(spaceData),
                timeout: 15000
            }).catch(() => null);

            if (response && response.ok) {
                const result = await response.json();
                if (result.success && result.image) {
                    return {
                        success: true,
                        image: result.image,
                        type: '3d_visualization'
                    };
                }
            }
            
            throw new Error('3D visualization service unavailable');
        } catch (error) {
            throw new Error(`3D visualization failed: ${error.message}`);
        }
    }

    /**
     * Display AI blueprint in UI
     */
    displayAIBlueprint(containerId, blueprintData) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        const imageUrl = `data:image/png;base64,${blueprintData.image}`;
        
        container.innerHTML = `
            <div class="ai-blueprint-card">
                <div class="blueprint-header">
                    <h3>
                        <i class="fas fa-robot"></i>
                        AI-Generated Blueprint
                        ${blueprintData.type === 'ai_generated' ? '<span class="ai-badge">AI</span>' : '<span class="ai-badge fallback">Procedural</span>'}
                    </h3>
                </div>
                <div class="blueprint-image">
                    <img src="${imageUrl}" alt="AI Generated Blueprint" />
                </div>
                ${blueprintData.prompt ? `
                <div class="blueprint-info">
                    <p><strong>AI Prompt Used:</strong></p>
                    <p class="prompt-text">${blueprintData.prompt}</p>
                </div>
                ` : ''}
                <div class="blueprint-actions">
                    <button onclick="vastuAI.downloadBlueprint('${imageUrl}', 'vastu-blueprint.png')" class="btn-download">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Display layout suggestions in UI
     */
    displayLayoutSuggestions(containerId, suggestionsData) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        let html = `
            <div class="layout-suggestions">
                <h3>
                    <i class="fas fa-lightbulb"></i>
                    AI Layout Suggestions
                    <span class="method-badge">${suggestionsData.method === 'ai_enhanced' ? 'AI Enhanced' : 'Rule-Based'}</span>
                </h3>
        `;

        if (suggestionsData.suggestions && suggestionsData.suggestions.length > 0) {
            html += '<div class="suggestions-list">';
            
            suggestionsData.suggestions.forEach(suggestion => {
                const scoreColor = suggestion.score >= 90 ? 'green' : suggestion.score >= 70 ? 'orange' : 'red';
                
                html += `
                    <div class="suggestion-card">
                        <div class="suggestion-header">
                            <h4>${suggestion.room}</h4>
                            <span class="score-badge" style="background: ${scoreColor}">
                                ${suggestion.score}%
                            </span>
                        </div>
                        <div class="suggestion-body">
                            <p><strong>Current:</strong> ${suggestion.current_zone || 'Not specified'}</p>
                            <p><strong>Ideal:</strong> <span class="ideal-zone">${suggestion.ideal_zone}</span></p>
                            ${suggestion.alternatives.length > 0 ? `
                                <p><strong>Alternatives:</strong> ${suggestion.alternatives.join(', ')}</p>
                            ` : ''}
                            ${suggestion.avoid.length > 0 ? `
                                <p><strong>Avoid:</strong> <span class="avoid-zone">${suggestion.avoid.join(', ')}</span></p>
                            ` : ''}
                            <p class="reasoning">${suggestion.reasoning}</p>
                            <div class="elements-tags">
                                ${suggestion.elements.map(el => `<span class="element-tag element-${el}">${el}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        }

        if (suggestionsData.ai_enhanced) {
            html += `
                <div class="ai-insights">
                    <h4>AI Enhanced Insights:</h4>
                    <div class="ai-text">${suggestionsData.ai_enhanced}</div>
                </div>
            `;
        }

        html += '</div>';
        container.innerHTML = html;
    }

    /**
     * Display energy heatmap in UI
     */
    displayEnergyHeatmap(containerId, heatmapData) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        const imageUrl = `data:image/png;base64,${heatmapData.heatmap}`;
        
        let elementBalanceHtml = '';
        if (heatmapData.element_balance) {
            const elements = ['fire', 'water', 'earth', 'air', 'space'];
            elementBalanceHtml = '<div class="element-balance">';
            
            elements.forEach(element => {
                const balance = heatmapData.element_balance[element] * 100;
                elementBalanceHtml += `
                    <div class="element-balance-item">
                        <span class="element-name">${element}</span>
                        <div class="balance-bar">
                            <div class="balance-fill element-${element}" style="width: ${balance}%"></div>
                        </div>
                        <span class="balance-value">${balance.toFixed(1)}%</span>
                    </div>
                `;
            });
            
            elementBalanceHtml += '</div>';
        }

        container.innerHTML = `
            <div class="energy-heatmap-card">
                <div class="heatmap-header">
                    <h3>
                        <i class="fas fa-fire"></i>
                        Energy Balance Heatmap
                    </h3>
                </div>
                <div class="heatmap-image">
                    <img src="${imageUrl}" alt="Energy Heatmap" />
                </div>
                ${elementBalanceHtml}
                <div class="heatmap-actions">
                    <button onclick="vastuAI.downloadBlueprint('${imageUrl}', 'energy-heatmap.png')" class="btn-download">
                        <i class="fas fa-download"></i> Download Heatmap
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Download blueprint/heatmap
     */
    downloadBlueprint(imageUrl, filename) {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Initialize global instance
const vastuAI = new VastuAIIntegration();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VastuAIIntegration;
}

