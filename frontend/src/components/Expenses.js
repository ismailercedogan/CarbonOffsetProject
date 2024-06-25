import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Expenses = () => {
  const [expenses, setExpenses] = useState({});
  const [selectedMonth, setSelectedMonth] = useState('');

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const response = await axios.get('http://localhost:5000/expenses', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setExpenses(response.data);
      } catch (error) {
        console.error('Error fetching expenses:', error);
      }
    };

    fetchExpenses();
  }, []);

  const handleMonthClick = (month) => {
    setSelectedMonth(month);
  };

  return (
    <div className="expenses">
      <h2>Expenses</h2>
      <div>
        {Object.keys(expenses).map((month) => (
          <button key={month} onClick={() => handleMonthClick(month)}>
            {month}
          </button>
        ))}
      </div>
      {selectedMonth && (
        <div>
          <h3>Expenses for {selectedMonth}</h3>
          <ul>
            {Object.entries(expenses[selectedMonth]).map(([category, amount]) => (
              <li key={category}>
                {category}: {amount}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Expenses;
