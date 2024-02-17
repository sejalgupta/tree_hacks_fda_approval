import React, { useState } from 'react';

export default function DeviceForm() {
  const [deviceDescription, setDeviceDescription] = useState('');
  const [intendedUse, setIntendedUse] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Implement what should happen on form submission, e.g., sending data to an API
  };

  return (
    <div className="max-w-lg mx-auto mt-10 p-8 bg-white shadow-lg rounded-lg">
      <h1 className="text-2xl font-bold text-center mb-6">Device Information Form</h1>
      <p className="text-center mb-8 text-gray-600">
        Please fill in the details about your device and its intended use.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4 p-4 border rounded-lg flex flex-col">
          <label htmlFor="device-description" className="mb-2 text-sm font-medium text-gray-700">
            What is your device description?
          </label>
          <input
            type="text"
            name="device-description"
            id="device-description"
            required
            value={deviceDescription}
            onChange={(e) => setDeviceDescription(e.target.value)}
            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
        </div>

        <div className="mb-6 p-4 border rounded-lg flex flex-col">
          <label htmlFor="intended-use" className="mb-2 text-sm font-medium text-gray-700">
            What is your intended use?
          </label>
          <input
            type="text"
            name="intended-use"
            id="intended-use"
            required
            value={intendedUse}
            onChange={(e) => setIntendedUse(e.target.value)}
            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
        </div>

        <div className="flex justify-between mt-6">
          <button
            type="submit"
            className="inline-flex items-center justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
