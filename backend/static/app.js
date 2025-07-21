// API base URL - uses relative paths so it works everywhere
   const API_BASE = '';

   // Show error message
   function showError(message) {
     const errorEl = document.getElementById('errorMessage');
     errorEl.textContent = message;
     errorEl.style.display = 'block';
     setTimeout(() => errorEl.style.display = 'none', 5000);
   }

   // Show success message
   function showSuccess(message) {
     const successEl = document.getElementById('successMessage');
     successEl.textContent = message;
     successEl.style.display = 'block';
     setTimeout(() => successEl.style.display = 'none', 3000);
   }

   // Format date nicely
   function formatDate(dateString) {
     const date = new Date(dateString);
     return date.toLocaleDateString('en-US', {
       year: 'numeric',
       month: 'short',
       day: 'numeric',
       hour: '2-digit',
       minute: '2-digit'
     });
   }

   // Update statistics
   function updateStats(logs) {
     const totalWeight = logs.reduce((sum, log) => sum + log.weight, 0);
     const totalEntries = logs.length;
     const co2Reduced = (totalWeight * 0.89).toFixed(1); // Approximate CO2 reduction factor

     document.getElementById('totalWeight').textContent = `${totalWeight.toFixed(1)} kg`;
     document.getElementById('totalEntries').textContent = totalEntries;
     document.getElementById('co2Reduced').textContent = `${co2Reduced} kg`;
   }

   // Fetch and display logs
   async function fetchLogs() {
     try {
       console.log('Fetching logs...');
       const response = await fetch(`${API_BASE}/api/logs`);
       
       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }
       
       const logs = await response.json();
       console.log('Received logs:', logs);
       
       const logsList = document.getElementById('logsList');
       
       if (logs.length === 0) {
         logsList.innerHTML = '<li class="empty-state">No compost logs yet. Start tracking your composting journey!</li>';
         updateStats([]);
         return;
       }
       
       logsList.innerHTML = logs.map(log => `
         <li class="log-item">
           <div class="log-info">
             <div class="log-weight">${log.weight} kg</div>
             <div class="log-location">📍 ${log.location}</div>
             <div class="log-date">${formatDate(log.timestamp)}</div>
           </div>
           <button class="delete-btn" onclick="deleteLog(${log.id})" title="Delete this entry">
             🗑️
           </button>
         </li>
       `).join('');
       
       updateStats(logs);
     } catch (error) {
       console.error('Error fetching logs:', error);
       showError('Failed to load compost logs. Please try again.');
     }
   }

   // Delete a log entry
   async function deleteLog(logId) {
     if (!confirm('Are you sure you want to delete this entry?')) {
       return;
     }
     
     try {
       const response = await fetch(`${API_BASE}/api/logs/${logId}`, {
         method: 'DELETE'
       });
       
       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }
       
       const result = await response.json();
       console.log('Log deleted:', result);
       
       showSuccess('Entry deleted successfully!');
       fetchLogs(); // Refresh the list
     } catch (error) {
       console.error('Error deleting log:', error);
       showError('Failed to delete entry. Please try again.');
     }
   }

   // Handle form submission
   document.getElementById('compostForm').addEventListener('submit', async (e) => {
     e.preventDefault();
     
     const weight = parseFloat(document.getElementById('weight').value);
     const location = document.getElementById('location').value.trim();
     
     if (!weight || weight <= 0) {
       showError('Please enter a valid weight.');
       return;
     }
     
     if (!location) {
       showError('Please enter a location.');
       return;
     }
     
     try {
       console.log('Submitting:', { weight, location });
       const response = await fetch(`${API_BASE}/api/log`, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({ weight, location })
       });
       
       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }
       
       const result = await response.json();
       console.log('Log added:', result);
       
       showSuccess('Compost entry added successfully!');
       
       // Clear form
       document.getElementById('compostForm').reset();
       
       // Refresh logs
       fetchLogs();
     } catch (error) {
       console.error('Error adding log:', error);
       showError('Failed to add compost entry. Please try again.');
     }
   });

   // Test API connection on load
   async function testConnection() {
     try {
       const response = await fetch(`${API_BASE}/api/test`);
       const data = await response.json();
       console.log('API Test:', data);
     } catch (error) {
       console.error('API connection test failed:', error);
     }
   }

   // Initialize on page load
   document.addEventListener('DOMContentLoaded', () => {
     console.log('Page loaded, initializing...');
     testConnection();
     fetchLogs();
   });