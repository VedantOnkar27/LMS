import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const XMLOperations = ({ libraryId, onRefresh }) => {
  const [xmlContent, setXmlContent] = useState('');
  const [showXmlModal, setShowXmlModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleExport = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    try {
      const response = await axios.get(`${BACKEND_URL}/api/library/${libraryId}/xml/export`);
      setXmlContent(response.data.xml);
      setShowXmlModal(true);
      setMessage({ type: 'success', text: 'XML exported successfully!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to export XML' });
    }
    setLoading(false);
  };

  const handleImport = async () => {
    if (!xmlContent.trim()) {
      setMessage({ type: 'error', text: 'Please enter XML content to import' });
      return;
    }
    
    setLoading(true);
    setMessage({ type: '', text: '' });
    try {
      await axios.post(`${BACKEND_URL}/api/library/${libraryId}/xml/import`, { xml: xmlContent });
      setMessage({ type: 'success', text: 'XML imported successfully!' });
      setXmlContent('');
      if (onRefresh) onRefresh();
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to import XML' });
    }
    setLoading(false);
  };

  const handleSync = async (source, target) => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    try {
      const response = await axios.post(`${BACKEND_URL}/api/library/xml/sync`, {
        source,
        target
      });
      setMessage({ type: 'success', text: response.data.message });
      if (onRefresh) onRefresh();
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to sync libraries' });
    }
    setLoading(false);
  };

  const downloadXml = () => {
    const blob = new Blob([xmlContent], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `library_${libraryId}_export.xml`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">XML Data Operations</h2>
      
      {message.text && (
        <div className={`p-4 rounded-lg mb-4 ${
          message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Export/Import Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-700">Export / Import</h3>
          <button
            onClick={handleExport}
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Exporting...' : `Export Library ${libraryId.toUpperCase()} to XML`}
          </button>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              XML Content to Import:
            </label>
            <textarea
              value={xmlContent}
              onChange={(e) => setXmlContent(e.target.value)}
              className="w-full h-32 border border-gray-300 rounded-lg p-2 font-mono text-xs"
              placeholder="Paste XML content here..."
            />
          </div>
          
          <button
            onClick={handleImport}
            disabled={loading || !xmlContent.trim()}
            className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Importing...' : `Import XML to Library ${libraryId.toUpperCase()}`}
          </button>
        </div>

        {/* Sync Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-700">Sync Libraries</h3>
          <div className="bg-gray-50 p-4 rounded-lg space-y-3">
            <p className="text-sm text-gray-600 mb-3">Synchronize data between libraries:</p>
            
            <button
              onClick={() => handleSync('a', 'b')}
              disabled={loading}
              className="w-full bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
            >
              {loading ? 'Syncing...' : 'Sync Library A → Library B'}
            </button>
            
            <button
              onClick={() => handleSync('b', 'a')}
              disabled={loading}
              className="w-full bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
            >
              {loading ? 'Syncing...' : 'Sync Library B → Library A'}
            </button>
            
            <div className="text-xs text-gray-500 mt-2">
              <p>• One-way sync: Source → Target</p>
              <p>• Duplicates are merged based on ID</p>
              <p>• Target library data is preserved</p>
            </div>
          </div>
        </div>
      </div>

      {/* XML Preview Modal */}
      {showXmlModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[80vh] flex flex-col">
            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-xl font-bold text-gray-800">XML Export Preview</h3>
              <button
                onClick={() => setShowXmlModal(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>
            <div className="p-4 overflow-auto flex-1 scrollbar-thin">
              <pre className="bg-gray-50 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                {xmlContent}
              </pre>
            </div>
            <div className="p-4 border-t border-gray-200 flex space-x-3">
              <button
                onClick={downloadXml}
                className="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition"
              >
                Download XML
              </button>
              <button
                onClick={() => navigator.clipboard.writeText(xmlContent)}
                className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition"
              >
                Copy to Clipboard
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default XMLOperations;