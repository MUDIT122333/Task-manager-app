import React, { useState, useEffect } from 'react';
import CreateTaskForm from '../components/CreateTaskForm';
import CreateProjectForm from '../components/CreateProjectForm';
import TaskStatusUpdate from '../components/TaskStatusUpdate';

const Dashboard = ({ user, onLogout }) => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0
  });
  const [loading, setLoading] = useState(true);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [showCreateProject, setShowCreateProject] = useState(false);

  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json'
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/users', {
        headers: getAuthHeaders()
      });

      const data = await res.json();

      if (res.ok) {
        setUsers(data.users);
      } else {
        console.error(data.error);
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
  };

  const fetchData = async () => {
    try {
      const [tasksRes, projectsRes] = await Promise.all([
        fetch('https://task-manager-backend-l0h5.onrender.com/api/tasks', { headers: getAuthHeaders() }),
        fetch('https://task-manager-backend-l0h5.onrender.com/api/projects', { headers: getAuthHeaders() })
      ]);

      const tasksData = await tasksRes.json();
      const projectsData = await projectsRes.json();

      if (tasksRes.ok) {
        setTasks(tasksData.tasks);
        calculateStats(tasksData.tasks);
      }

      if (projectsRes.ok) {
        setProjects(projectsData.projects);
      }

      await fetchUsers();
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (taskList) => {
    const now = new Date();
    const stats = {
      total: taskList.length,
      completed: taskList.filter(t => t.status === 'DONE').length,
      pending: taskList.filter(t => t.status === 'TODO').length,
      overdue: taskList.filter(t => {
        return t.deadline && new Date(t.deadline) < now && t.status !== 'DONE';
      }).length
    };
    setStats(stats);
  };

  
  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'HIGH': return 'priority-high';
      case 'MEDIUM': return 'priority-medium';
      case 'LOW': return 'priority-low';
      default: return '';
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks([...tasks, newTask]);
    calculateStats([...tasks, newTask]);
  };

  const handleProjectCreated = (newProject) => {
    setProjects([...projects, newProject]);
  };

  const handleTaskStatusUpdate = (updatedTask) => {
    const updatedTasks = tasks.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    );
    setTasks(updatedTasks);
    calculateStats(updatedTasks);
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1 className="dashboard-title">Task Manager Dashboard</h1>
          <div>
            <span style={{ marginRight: '1rem' }}>Welcome, {user?.username} ({user?.role})</span>
            <button className="btn btn-danger" onClick={onLogout}>Logout</button>
          </div>
        </div>

        <div className="dashboard-content">
          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">{stats.total}</div>
              <div className="stat-label">Total Tasks</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.completed}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.pending}</div>
              <div className="stat-label">Pending</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.overdue}</div>
              <div className="stat-label">Overdue</div>
            </div>
          </div>

          {/* Admin Controls */}
          {user?.role === 'admin' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Admin Controls</h3>
              </div>
              <div className="card-body">
                <button 
                  className="btn btn-primary" 
                  style={{ marginRight: '1rem' }}
                  onClick={() => setShowCreateProject(true)}
                >
                  Create Project
                </button>
                <button 
                  className="btn btn-primary"
                  onClick={() => setShowCreateTask(true)}
                >
                  Create Task
                </button>
              </div>
            </div>
          )}

          {/* Tasks Table */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Your Tasks</h3>
            </div>
            <div className="card-body">
              {tasks.length === 0 ? (
                <p>No tasks assigned to you.</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Project</th>
                      <th>Status</th>
                      <th>Priority</th>
                      <th>Deadline</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tasks.map(task => (
                      <tr key={task.id}>
                        <td>{task.title}</td>
                        <td>{task.project_name}</td>
                        <td>
                          <TaskStatusUpdate 
                            task={task} 
                            onStatusUpdate={handleTaskStatusUpdate}
                          />
                        </td>
                        <td>
                          <span className={`status-badge ${getPriorityClass(task.priority)}`}>
                            {task.priority}
                          </span>
                        </td>
                        <td>
                          {task.deadline ? new Date(task.deadline).toLocaleDateString() : 'No deadline'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>

          {/* Projects List */}
          {user?.role === 'admin' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Projects</h3>
              </div>
              <div className="card-body">
                {projects.length === 0 ? (
                  <p>No projects created yet.</p>
                ) : (
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Tasks</th>
                        <th>Created By</th>
                      </tr>
                    </thead>
                    <tbody>
                      {projects.map(project => (
                        <tr key={project.id}>
                          <td>{project.name}</td>
                          <td>{project.description || 'No description'}</td>
                          <td>{project.task_count}</td>
                          <td>{project.creator_name}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Create Task Form Modal */}
      {showCreateTask && (
        <CreateTaskForm
          projects={projects}
          users={users}
          onClose={() => setShowCreateTask(false)}
          onTaskCreated={handleTaskCreated}
        />
      )}
      
      {/* Create Project Form Modal */}
      {showCreateProject && (
        <CreateProjectForm
          onClose={() => setShowCreateProject(false)}
          onProjectCreated={handleProjectCreated}
        />
      )}
    </>
  );
};

export default Dashboard;
