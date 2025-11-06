import React, { useState } from 'react';
import './App.css';
import LibraryDashboard from './components/LibraryDashboard';
import XMLOperations from './components/XMLOperations';
import OOPVisualization from './components/OOPVisualization';

function App() {
  const [selectedLibrary, setSelectedLibrary] = useState('a');
  const [activeView, setActiveView] = useState('dashboard');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="gradient-bg text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold mb-2">Library Management System</h1>
          <p className="text-blue-100">Object-Oriented Database with XML Data Sharing</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between py-4">
            {/* Library Selector */}
            <div className="flex items-center space-x-4">
              <span className="text-gray-700 font-semibold">Select Library:</span>
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setSelectedLibrary('a')}
                  className={`px-6 py-2 rounded-lg font-semibold transition ${
                    selectedLibrary === 'a'
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Library A
                </button>
                <button
                  onClick={() => setSelectedLibrary('b')}
                  className={`px-6 py-2 rounded-lg font-semibold transition ${
                    selectedLibrary === 'b'
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Library B
                </button>
              </div>
            </div>

            {/* View Selector */}
            <div className="flex space-x-2">
              <button
                onClick={() => setActiveView('dashboard')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  activeView === 'dashboard'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                📚 Dashboard
              </button>
              <button
                onClick={() => setActiveView('xml')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  activeView === 'xml'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                🔄 XML Operations
              </button>
              <button
                onClick={() => setActiveView('oop')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  activeView === 'oop'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                🎓 OOP Concepts
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-fade-in">
          {activeView === 'dashboard' && (
            <LibraryDashboard 
              libraryId={selectedLibrary} 
              refreshTrigger={refreshTrigger}
            />
          )}
          
          {activeView === 'xml' && (
            <XMLOperations 
              libraryId={selectedLibrary}
              onRefresh={handleRefresh}
            />
          )}
          
          {activeView === 'oop' && (
            <OOPVisualization />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-gray-600">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Key Features</h3>
              <ul className="space-y-1">
                <li>• Object-Oriented Database Design</li>
                <li>• XML Data Import/Export</li>
                <li>• Cross-Library Synchronization</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">OOP Principles</h3>
              <ul className="space-y-1">
                <li>• Inheritance (Person → Student/Teacher)</li>
                <li>• Polymorphism (Different borrow rules)</li>
                <li>• Encapsulation (Protected data access)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Technology Stack</h3>
              <ul className="space-y-1">
                <li>• FastAPI Backend</li>
                <li>• MongoDB Database</li>
                <li>• React Frontend</li>
              </ul>
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-gray-200 text-center text-gray-500">
            <p>© 2024 Library Management System - Demonstrating OOP Concepts</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
