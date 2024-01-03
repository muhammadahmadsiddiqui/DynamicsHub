import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const FlashMessage = ({ message, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 8000); // Adjust the time as needed (e.g., 8000ms = 8 seconds)

    return () => {
      clearTimeout(timer);
    };
  }, [onClose]);

  return (
    <div className="flash-message">
      {message}
    </div>
  );
};

const CreateData = () => {
  const [carId, setCarId] = useState('');
  const [brandName, setBrandName] = useState('');
  const [color, setColor] = useState('');
  const [flashMessage, setFlashMessage] = useState('');

  const handleCreate = async () => {
    try {
      await axios.post('http://localhost:8000/create-dynamics-data/', null, {
        params: {
          CarId: carId,
          BrandName: brandName,
          Color: color,
        },
      });
      setCarId(''); // Clear input fields after successful creation
      setBrandName('');
      setColor('');
      setFlashMessage('Record created successfully!'); // Trigger the flash message
      window.location.reload(); // Reload the page
    } catch (error) {
      console.error('Error creating data:', error);
    }
  
  };

  const handleCloseFlashMessage = () => {
    setFlashMessage('');
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-lg-6">
          <div className="form-container">
            <h2>Create New Car Entry</h2>
            {flashMessage && <FlashMessage message={flashMessage} onClose={handleCloseFlashMessage} />}
            <div className="form-group">
              <label>Car Id:</label>
              <input type="text" value={carId} onChange={(e) => setCarId(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Brand Name:</label>
              <input type="text" value={brandName} onChange={(e) => setBrandName(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Color:</label>
              <input type="text" value={color} onChange={(e) => setColor(e.target.value)} />
            </div>
            <button className="btn btn-warning" onClick={handleCreate}>Create</button>
          </div>
        </div>
      </div>
    </div>
  );
};


// get data

const DynamicsData = () => {
  const [data, setData] = useState([]);
  const [flashMessage, setFlashMessage] = useState('');
  const [selectedRow, setSelectedRow] = useState(null); // New state for selected row


  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/get-dynamics-data/');
        setData(response.data.value); // Set the 'value' array as the state data
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const handleDelete = async (dataAreaId, carId) => {
    try {
      await axios.delete(`http://localhost:8000/delete-dynamics-data/${dataAreaId}/${carId}`);
      const response = await axios.get('http://localhost:8000/get-dynamics-data/');

      setData(response.data.value);
      setFlashMessage('Record deleted successfully!'); // Trigger the flash message
    } catch (error) {
      console.error('Error deleting data:', error);
    }
  };

  const handleCloseFlashMessage = () => {
    setFlashMessage('');
  };

  
// update data

const UpdateData = ({ dataAreaId, carId }) => {
  const [updatedBrandName, setUpdatedBrandName] = useState('');
  const [updatedColor, setUpdatedColor] = useState('');

  const handleUpdate = async () => {
    try {
      await axios.put(`http://localhost:8000/update-dynamics-data/${dataAreaId}/${carId}/`, {
        BrandName: updatedBrandName,
        Color: updatedColor,
      });
      // Handle success - maybe display a success message or update the data
      const response = await axios.get('http://localhost:8000/get-dynamics-data/');
  
      setSelectedRow(null); // Clear the selected row state
      setData(response.data.value);
      
      // Trigger the flash message
      setFlashMessage('Record updated successfully!');
    } catch (error) {
      console.error('Error updating data:', error);
    }
  };

  return (
    <div className="form-container">
      <h2>Update Car Entry</h2>
      <div className="form-group">
        <label>New Brand Name:</label>
        <input type="text" value={updatedBrandName} onChange={(e) => setUpdatedBrandName(e.target.value)} />
      </div>
      <div className="form-group">
        <label>New Color:</label>
        <input type="text" value={updatedColor} onChange={(e) => setUpdatedColor(e.target.value)} />
      </div>
      <button className="btn btn-primary" onClick={handleUpdate}>
        Update
      </button>
    </div>
  );
};

const handleUpdateClick = (dataAreaId, carId) => {
  setSelectedRow(carId); // Set the selected row to show the update form
};


  return (
    <div className="container">
      {flashMessage && <FlashMessage message={flashMessage} onClose={handleCloseFlashMessage} />}
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Car Id</th>
                  <th>Brand Name</th>
                  <th>Color</th>
                  <th>Delete</th>
                  <th>Update</th>
                </tr>
              </thead>
              <tbody>
                {data.map(item => (
                  <tr key={item.CarId}>
                    <td>{item.CarId}</td>
                    <td>{item.BrandName}</td>
                    <td>{item.Color}</td>
                    <td>
                      <button className="btn btn-danger" onClick={() => handleDelete(item.dataAreaId, item.CarId)}>
                        Delete
                      </button>
                    </td>
                    <td>
                      {selectedRow === item.CarId ? ( // Show update form for selected row
                        <UpdateData dataAreaId={item.dataAreaId} carId={item.CarId} />
                      ) : (
                        <button className="btn btn-primary" onClick={() => handleUpdateClick(item.dataAreaId, item.CarId)}>
                          Update
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};


function App() {
  return (
    <div className="App">
      <header>
        <DynamicsData />
        <div className='center-text margin-top'>
          <CreateData/>
        </div>
      </header>
    </div>
  );
}

export default App;