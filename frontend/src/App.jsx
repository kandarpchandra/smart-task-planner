import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL;
function App() {
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);

  // Fetch all plans on load
  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/plans`);
      setPlans(response.data.plans);
    } catch (error) {
      console.error('Error fetching plans:', error);
    }
  };

  const createPlan = async (e) => {
    e.preventDefault();
    if (!goal.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/plan?goal=${encodeURIComponent(goal)}`);
      alert('Plan created successfully!');
      setGoal('');
      fetchPlans();
      viewPlan(response.data.plan_id);
    } catch (error) {
      console.error('Error creating plan:', error);
      alert('Error creating plan. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const viewPlan = async (planId) => {
    try {
      const response = await axios.get(`${API_URL}/api/plan/${planId}`);
      setSelectedPlan(response.data);
    } catch (error) {
      console.error('Error fetching plan:', error);
    }
  };

  const updateTaskStatus = async (planId, taskNumber, newStatus) => {
    try {
      await axios.patch(`${API_URL}/api/task/${planId}/${taskNumber}/status?status=${newStatus}`);
      viewPlan(planId); // Refresh the plan view
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const downloadCSV = (planId) => {
    window.open(`${API_URL}/api/plan/${planId}/export/csv`, '_blank');
  };

  const deletePlan = async (planId) => {
    if (!window.confirm('Are you sure you want to delete this plan?')) return;
    
    try {
      await axios.delete(`${API_URL}/api/plan/${planId}`);
      alert('Plan deleted successfully!');
      setSelectedPlan(null);
      fetchPlans();
    } catch (error) {
      console.error('Error deleting plan:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Smart Task Planner</h1>
        <p>AI-Powered Task Breakdown System</p>
      </header>

      <div className="container">
        {/* Create New Plan Section */}
        <div className="create-section">
          <h2>Create New Plan</h2>
          <form onSubmit={createPlan}>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Enter your goal (e.g., Build a mobile app)"
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Generating Plan...' : 'Generate Plan'}
            </button>
          </form>
        </div>

        {/* Plans List */}
        <div className="plans-section">
          <h2>Your Plans ({plans.length})</h2>
          <div className="plans-list">
            {plans.map((plan) => (
              <div key={plan.id} className="plan-card">
                <h3>{plan.goal}</h3>
                <p>{plan.task_count} tasks</p>
                <button onClick={() => viewPlan(plan.id)}>View Details</button>
              </div>
            ))}
            {plans.length === 0 && <p className="empty-message">No plans yet. Create one above!</p>}
          </div>
        </div>

        {/* Plan Details */}
        {selectedPlan && (
          <div className="plan-details">
            <div className="plan-header">
              <h2>📋 {selectedPlan.goal}</h2>
              <div className="plan-actions">
                <button onClick={() => downloadCSV(selectedPlan.id)} className="download-btn">
                  📥 Download CSV
                </button>
                <button onClick={() => deletePlan(selectedPlan.id)} className="delete-btn">
                  🗑️ Delete Plan
                </button>
              </div>
            </div>
            
            <div className="progress-bar-container">
              <div className="progress-bar" style={{width: `${selectedPlan.progress}%`}}>
                {selectedPlan.progress}% Complete
              </div>
            </div>

            <div className="tasks-list">
              {selectedPlan.tasks.map((task) => (
                <div key={task.id} className={`task-card ${task.status}`}>
                  <div className="task-header">
                    <h3>
                      <span className="task-number">#{task.id}</span>
                      {task.name}
                    </h3>
                    <span className={`priority-badge ${task.priority.toLowerCase()}`}>
                      {task.priority}
                    </span>
                  </div>
                  
                  <p className="task-description">{task.description}</p>
                  
                  <div className="task-meta">
                    <span>⏱️ {task.estimated_days} days</span>
                    {task.dependencies.length > 0 && (
                      <span>🔗 Depends on: {task.dependencies.join(', ')}</span>
                    )}
                  </div>

                  <div className="task-status">
                    <label>Status:</label>
                    <select
                      value={task.status}
                      onChange={(e) => updateTaskStatus(selectedPlan.id, task.id, e.target.value)}
                    >
                      <option value="pending">⏳ Pending</option>
                      <option value="in_progress">🔄 In Progress</option>
                      <option value="completed">✅ Completed</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
