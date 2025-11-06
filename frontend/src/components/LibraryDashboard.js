import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const LibraryDashboard = ({ libraryId, refreshTrigger }) => {
  const [activeTab, setActiveTab] = useState('books');
  const [data, setData] = useState({
    books: [],
    magazines: [],
    students: [],
    teachers: [],
    borrowRecords: [],
    stats: {}
  });
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showBorrowModal, setShowBorrowModal] = useState(false);
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchData();
  }, [libraryId, refreshTrigger]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [booksRes, magazinesRes, studentsRes, teachersRes, recordsRes, statsRes] = await Promise.all([
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/books`),
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/magazines`),
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/students`),
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/teachers`),
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/borrow-records`),
        axios.get(`${BACKEND_URL}/api/library/${libraryId}/stats`)
      ]);

      setData({
        books: booksRes.data.books,
        magazines: magazinesRes.data.magazines,
        students: studentsRes.data.students,
        teachers: teachersRes.data.teachers,
        borrowRecords: recordsRes.data.records,
        stats: statsRes.data
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setLoading(false);
  };

  const handleAdd = async () => {
    try {
      const endpoint = activeTab === 'books' || activeTab === 'magazines' 
        ? `${BACKEND_URL}/api/library/${libraryId}/${activeTab}`
        : `${BACKEND_URL}/api/library/${libraryId}/${activeTab}`;
      
      await axios.post(endpoint, formData);
      setMessage({ type: 'success', text: `${activeTab.slice(0, -1)} added successfully!` });
      setShowAddModal(false);
      setFormData({});
      fetchData();
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to add item' });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    
    try {
      await axios.delete(`${BACKEND_URL}/api/library/${libraryId}/${activeTab}/${id}`);
      setMessage({ type: 'success', text: 'Item deleted successfully!' });
      fetchData();
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to delete item' });
    }
  };

  const handleBorrow = async () => {
    try {
      await axios.post(`${BACKEND_URL}/api/library/${libraryId}/borrow`, formData);
      setMessage({ type: 'success', text: 'Item borrowed successfully!' });
      setShowBorrowModal(false);
      setFormData({});
      fetchData();
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to borrow item' });
    }
  };

  const handleReturn = async (recordId) => {
    try {
      await axios.post(`${BACKEND_URL}/api/library/${libraryId}/return`, { record_id: recordId });
      setMessage({ type: 'success', text: 'Item returned successfully!' });
      fetchData();
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to return item' });
    }
  };

  const openAddModal = (tab) => {
    setActiveTab(tab);
    setFormData({});
    setShowAddModal(true);
  };

  const renderStats = () => (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">Total Books</p>
        <p className="text-2xl font-bold text-blue-600">{data.stats.total_books || 0}</p>
      </div>
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">Available Books</p>
        <p className="text-2xl font-bold text-green-600">{data.stats.available_books || 0}</p>
      </div>
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">Total Members</p>
        <p className="text-2xl font-bold text-purple-600">
          {(data.stats.total_students || 0) + (data.stats.total_teachers || 0)}
        </p>
      </div>
      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">Active Borrows</p>
        <p className="text-2xl font-bold text-orange-600">{data.stats.active_borrows || 0}</p>
      </div>
    </div>
  );

  const renderTable = () => {
    let items = [];
    let columns = [];

    switch (activeTab) {
      case 'books':
        items = data.books;
        columns = ['Title', 'Author', 'Genre', 'Pages', 'Available', 'Actions'];
        break;
      case 'magazines':
        items = data.magazines;
        columns = ['Title', 'Author', 'Issue #', 'Month', 'Available', 'Actions'];
        break;
      case 'students':
        items = data.students;
        columns = ['Name', 'Student ID', 'Grade', 'Email', 'Max Borrow', 'Actions'];
        break;
      case 'teachers':
        items = data.teachers;
        columns = ['Name', 'Teacher ID', 'Department', 'Email', 'Max Borrow', 'Actions'];
        break;
      case 'records':
        items = data.borrowRecords;
        columns = ['Person', 'Item', 'Borrow Date', 'Due Date', 'Status', 'Actions'];
        break;
      default:
        items = [];
    }

    return (
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead className="bg-gray-100">
            <tr>
              {columns.map((col, idx) => (
                <th key={idx} className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {items.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-gray-500">
                  No items found. Click "Add New" to get started.
                </td>
              </tr>
            ) : (
              items.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  {activeTab === 'books' && (
                    <>
                      <td className="px-4 py-3 text-sm">{item.title}</td>
                      <td className="px-4 py-3 text-sm">{item.author}</td>
                      <td className="px-4 py-3 text-sm">{item.genre}</td>
                      <td className="px-4 py-3 text-sm">{item.pages}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          item.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {item.available ? 'Available' : 'Borrowed'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600 hover:text-red-800 font-semibold"
                        >
                          Delete
                        </button>
                      </td>
                    </>
                  )}
                  {activeTab === 'magazines' && (
                    <>
                      <td className="px-4 py-3 text-sm">{item.title}</td>
                      <td className="px-4 py-3 text-sm">{item.author}</td>
                      <td className="px-4 py-3 text-sm">{item.issue_number}</td>
                      <td className="px-4 py-3 text-sm">{item.publication_month}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          item.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {item.available ? 'Available' : 'Borrowed'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600 hover:text-red-800 font-semibold"
                        >
                          Delete
                        </button>
                      </td>
                    </>
                  )}
                  {activeTab === 'students' && (
                    <>
                      <td className="px-4 py-3 text-sm">{item.name}</td>
                      <td className="px-4 py-3 text-sm">{item.student_id}</td>
                      <td className="px-4 py-3 text-sm">{item.grade_level}</td>
                      <td className="px-4 py-3 text-sm">{item.email}</td>
                      <td className="px-4 py-3 text-sm">{item.max_borrow_limit}</td>
                      <td className="px-4 py-3 text-sm">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600 hover:text-red-800 font-semibold"
                        >
                          Delete
                        </button>
                      </td>
                    </>
                  )}
                  {activeTab === 'teachers' && (
                    <>
                      <td className="px-4 py-3 text-sm">{item.name}</td>
                      <td className="px-4 py-3 text-sm">{item.teacher_id}</td>
                      <td className="px-4 py-3 text-sm">{item.department}</td>
                      <td className="px-4 py-3 text-sm">{item.email}</td>
                      <td className="px-4 py-3 text-sm">{item.max_borrow_limit}</td>
                      <td className="px-4 py-3 text-sm">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600 hover:text-red-800 font-semibold"
                        >
                          Delete
                        </button>
                      </td>
                    </>
                  )}
                  {activeTab === 'records' && (
                    <>
                      <td className="px-4 py-3 text-sm">
                        {item.person_name}
                        <span className="text-xs text-gray-500 ml-1">({item.person_type})</span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {item.item_title}
                        <span className="text-xs text-gray-500 ml-1">({item.item_type})</span>
                      </td>
                      <td className="px-4 py-3 text-sm">{item.borrow_date}</td>
                      <td className="px-4 py-3 text-sm">{item.due_date}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          item.status === 'borrowed' ? 'bg-yellow-100 text-yellow-800' :
                          item.status === 'returned' ? 'bg-green-100 text-green-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {item.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {item.status === 'borrowed' && (
                          <button
                            onClick={() => handleReturn(item.id)}
                            className="text-blue-600 hover:text-blue-800 font-semibold"
                          >
                            Return
                          </button>
                        )}
                      </td>
                    </>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    );
  };

  const renderAddModal = () => {
    if (!showAddModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-2xl max-w-md w-full p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            Add New {activeTab.slice(0, -1).charAt(0).toUpperCase() + activeTab.slice(1, -1)}
          </h3>
          
          <div className="space-y-3">
            {activeTab === 'books' && (
              <>
                <input
                  type="text"
                  placeholder="Title"
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Author"
                  onChange={(e) => setFormData({...formData, author: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="ISBN"
                  onChange={(e) => setFormData({...formData, isbn: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Genre"
                  onChange={(e) => setFormData({...formData, genre: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="number"
                  placeholder="Pages"
                  onChange={(e) => setFormData({...formData, pages: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Publisher"
                  onChange={(e) => setFormData({...formData, publisher: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
              </>
            )}
            {activeTab === 'magazines' && (
              <>
                <input
                  type="text"
                  placeholder="Title"
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Author/Publisher"
                  onChange={(e) => setFormData({...formData, author: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="ISBN/Catalog Number"
                  onChange={(e) => setFormData({...formData, isbn: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Issue Number"
                  onChange={(e) => setFormData({...formData, issue_number: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Publication Month (e.g., January 2024)"
                  onChange={(e) => setFormData({...formData, publication_month: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
              </>
            )}
            {activeTab === 'students' && (
              <>
                <input
                  type="text"
                  placeholder="Name"
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Student ID"
                  onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Grade Level"
                  onChange={(e) => setFormData({...formData, grade_level: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="email"
                  placeholder="Email"
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="tel"
                  placeholder="Phone"
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
              </>
            )}
            {activeTab === 'teachers' && (
              <>
                <input
                  type="text"
                  placeholder="Name"
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Teacher ID"
                  onChange={(e) => setFormData({...formData, teacher_id: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="text"
                  placeholder="Department"
                  onChange={(e) => setFormData({...formData, department: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="email"
                  placeholder="Email"
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
                <input
                  type="tel"
                  placeholder="Phone"
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg p-2"
                />
              </>
            )}
          </div>

          <div className="flex space-x-3 mt-6">
            <button
              onClick={() => setShowAddModal(false)}
              className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-lg transition"
            >
              Cancel
            </button>
            <button
              onClick={handleAdd}
              className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition"
            >
              Add
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderBorrowModal = () => {
    if (!showBorrowModal) return null;

    const allItems = [...data.books, ...data.magazines].filter(item => item.available);
    const allPeople = [...data.students, ...data.teachers];

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-2xl max-w-md w-full p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Borrow Item</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Person:</label>
              <select
                onChange={(e) => setFormData({...formData, person_id: e.target.value})}
                className="w-full border border-gray-300 rounded-lg p-2"
              >
                <option value="">Choose a person...</option>
                {allPeople.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.name} ({person.person_type}) - Max: {person.max_borrow_limit}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Item:</label>
              <select
                onChange={(e) => setFormData({...formData, item_id: e.target.value})}
                className="w-full border border-gray-300 rounded-lg p-2"
              >
                <option value="">Choose an item...</option>
                {allItems.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.title} ({item.item_type})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex space-x-3 mt-6">
            <button
              onClick={() => setShowBorrowModal(false)}
              className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-lg transition"
            >
              Cancel
            </button>
            <button
              onClick={handleBorrow}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition"
            >
              Borrow
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          Library {libraryId.toUpperCase()} Dashboard
        </h2>
        <div className="flex space-x-2">
          {activeTab !== 'records' && (
            <button
              onClick={() => openAddModal(activeTab)}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition"
            >
              Add New
            </button>
          )}
          <button
            onClick={() => setShowBorrowModal(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition"
          >
            Borrow Item
          </button>
        </div>
      </div>

      {message.text && (
        <div className={`p-4 rounded-lg mb-4 ${
          message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {message.text}
        </div>
      )}

      {renderStats()}

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex space-x-8">
          {['books', 'magazines', 'students', 'teachers', 'records'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`py-2 px-1 font-semibold transition ${
                activeTab === tab
                  ? 'tab-active'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        renderTable()
      )}

      {renderAddModal()}
      {renderBorrowModal()}
    </div>
  );
};

export default LibraryDashboard;