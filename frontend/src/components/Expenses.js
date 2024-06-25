import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { Container, Row, Col, Card, CardBody, CardTitle, Button } from 'reactstrap';
import '../Expenses.css';

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const Expenses = () => {
  const [expenses, setExpenses] = useState({});
  const [selectedMonth, setSelectedMonth] = useState('');
  const [chartData, setChartData] = useState(null);
  const [totalExpense, setTotalExpense] = useState(0);

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
    const data = expenses[month];
    if (data) {
      const total = Object.values(data).reduce((sum, amount) => sum + amount, 0);
      setTotalExpense(total);
      setChartData({
        labels: Object.keys(data),
        datasets: [{
          label: 'Expenses',
          data: Object.values(data),
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        }],
      });
    }
  };

  return (
    <Container className="expenses">
      <h2>Expenses</h2>
      <Row className="mb-4">
        {Object.keys(expenses).map((month) => (
          <Col xs="auto" key={month}>
            <Button color="primary" onClick={() => handleMonthClick(month)}>
              {month}
            </Button>
          </Col>
        ))}
      </Row>
      {selectedMonth && (
        <Row>
          <Col md={6} className="mb-4">
            <h3>Expenses for {selectedMonth}</h3>
            <h4>Total Expense: ${totalExpense.toFixed(2)}</h4>
            <Row>
              {Object.entries(expenses[selectedMonth]).map(([category, amount]) => (
                <Col xs="12" md="6" key={category} className="mb-3">
                  <Card>
                    <CardBody>
                      <CardTitle tag="h5">{category}</CardTitle>
                      <p>Amount: ${amount}</p>
                    </CardBody>
                  </Card>
                </Col>
              ))}
            </Row>
          </Col>
          <Col md={6} className="mb-4">
            {chartData && (
              <div className="chart-container">
                <Bar data={chartData} />
              </div>
            )}
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default Expenses;
