import React, { useState } from 'react';

const TaskStatusUpdate = ({ task, onStatusUpdate }) => {
  const [loading, setLoading] = useState(false);

  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json'
  });

  const handleStatusChange = async (newStatus) => {
    setLoading(true);
    
    try {
      const response = await fetch(`https://task-manager-backend-l0h5.onrender.com/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ status: newStatus })
      });

      const data = await response.json();

      if (response.ok) {
        onStatusUpdate(data.task);
      } else {
        alert('Failed to update task status');
      }
    } catch (err) {
      alert('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'TODO': return 'status-todo';
      case 'IN PROGRESS': return 'status-progress';
      case 'DONE': return 'status-done';
      default: return '';
    }
  };

  return (
    <div>
      <span className={`status-badge ${getStatusClass(task.status)}`}>
        {task.status}
      </span>
      <select 
        value={task.status} 
        onChange={(e) => handleStatusChange(e.target.value)}
        disabled={loading}
        style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
      >
        <option value="TODO">TODO</option>
        <option value="IN PROGRESS">IN PROGRESS</option>
        <option value="DONE">DONE</option>
      </select>
    </div>
  );
};

export default TaskStatusUpdate;
