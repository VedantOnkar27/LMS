import React from 'react';

const OOPVisualization = () => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 animate-fade-in">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">OOP Concepts Visualization</h2>
      
      {/* Inheritance Diagram */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Inheritance Hierarchy</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Person Hierarchy */}
          <div className="border-2 border-blue-300 rounded-lg p-4">
            <div className="bg-blue-500 text-white p-3 rounded-md text-center mb-4">
              <span className="font-bold">Person (Base Class)</span>
              <p className="text-sm mt-1">id, name, email, phone</p>
            </div>
            <div className="flex flex-col space-y-3">
              <div className="bg-blue-200 p-3 rounded-md ml-8 border-l-4 border-blue-500">
                <span className="font-semibold">Student</span>
                <p className="text-xs text-gray-600">+ student_id, grade_level</p>
                <p className="text-xs text-blue-700">max_borrow_limit: 5</p>
              </div>
              <div className="bg-blue-200 p-3 rounded-md ml-8 border-l-4 border-blue-500">
                <span className="font-semibold">Teacher</span>
                <p className="text-xs text-gray-600">+ teacher_id, department</p>
                <p className="text-xs text-blue-700">max_borrow_limit: 10</p>
              </div>
            </div>
          </div>

          {/* Item Hierarchy */}
          <div className="border-2 border-green-300 rounded-lg p-4">
            <div className="bg-green-500 text-white p-3 rounded-md text-center mb-4">
              <span className="font-bold">Item (Base Class)</span>
              <p className="text-sm mt-1">id, title, author, isbn, available</p>
            </div>
            <div className="flex flex-col space-y-3">
              <div className="bg-green-200 p-3 rounded-md ml-8 border-l-4 border-green-500">
                <span className="font-semibold">Book</span>
                <p className="text-xs text-gray-600">+ genre, pages, publisher</p>
              </div>
              <div className="bg-green-200 p-3 rounded-md ml-8 border-l-4 border-green-500">
                <span className="font-semibold">Magazine</span>
                <p className="text-xs text-gray-600">+ issue_number, publication_month</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Polymorphism Examples */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Polymorphism in Action</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-purple-50 border border-purple-300 rounded-lg p-4">
            <h4 className="font-semibold text-purple-700 mb-2">Different Borrow Limits</h4>
            <p className="text-sm text-gray-600">Students can borrow up to 5 items, while Teachers can borrow up to 10 items - same method, different behavior!</p>
          </div>
          <div className="bg-purple-50 border border-purple-300 rounded-lg p-4">
            <h4 className="font-semibold text-purple-700 mb-2">Item Types</h4>
            <p className="text-sm text-gray-600">Books and Magazines are both Items but have different properties - demonstrating polymorphic behavior.</p>
          </div>
          <div className="bg-purple-50 border border-purple-300 rounded-lg p-4">
            <h4 className="font-semibold text-purple-700 mb-2">Person Types</h4>
            <p className="text-sm text-gray-600">Students and Teachers share common Person attributes but have unique identification and roles.</p>
          </div>
        </div>
      </div>

      {/* Encapsulation */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Encapsulation</h3>
        <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-4">
          <p className="text-sm text-gray-700">
            All classes use <span className="font-mono bg-gray-200 px-2 py-1 rounded">private fields</span> with 
            <span className="font-mono bg-gray-200 px-2 py-1 rounded mx-1">public getters/setters</span> through the API.
            Data integrity is maintained through controlled access patterns.
          </p>
        </div>
      </div>

      {/* Composition */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Composition</h3>
        <div className="bg-orange-50 border border-orange-300 rounded-lg p-4">
          <div className="flex items-center justify-center space-x-4">
            <div className="bg-blue-400 text-white p-3 rounded-md">Person</div>
            <span className="text-2xl">+</span>
            <div className="bg-green-400 text-white p-3 rounded-md">Item</div>
            <span className="text-2xl">=</span>
            <div className="bg-orange-400 text-white p-3 rounded-md">BorrowRecord</div>
          </div>
          <p className="text-sm text-gray-700 text-center mt-3">
            BorrowRecord combines Person and Item references, demonstrating composition relationships
          </p>
        </div>
      </div>
    </div>
  );
};

export default OOPVisualization;
