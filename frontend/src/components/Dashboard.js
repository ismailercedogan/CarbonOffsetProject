import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input, Container, Row, Col } from 'reactstrap';
import '../App.css';

Chart.register(ArcElement, Tooltip, Legend);

const Dashboard = () => {
  const [emissions, setEmissions] = useState({});
  const [recommendation, setRecommendation] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [rating, setRating] = useState(0);
  const [totalEmission, setTotalEmission] = useState(0);
  const [maxEmissionCategory, setMaxEmissionCategory] = useState('');
  const [warning, setWarning] = useState('');

  useEffect(() => {
    const fetchEmissions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/calculate-emissions', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const emissionsData = response.data;
        setEmissions(emissionsData);

        // Calculate total emissions and max emission category
        const currentMonth = new Date().toISOString().slice(0, 7); // Format: YYYY-MM
        const dataForCurrentMonth = emissionsData[currentMonth] || [];
        const total = dataForCurrentMonth.reduce((sum, e) => sum + e.emission, 0);
        const maxCategory = dataForCurrentMonth.reduce((max, e) => e.emission > max.emission ? e : max, { category: '', emission: 0 });

        setTotalEmission(total);
        setMaxEmissionCategory(maxCategory.category ? `${maxCategory.category} (${maxCategory.emission.toFixed(2)} kg CO2)` : 'N/A');

      } catch (error) {
        console.error('Error fetching emissions:', error);
      }
    };

    fetchEmissions();
  }, []);

  const fetchRecommendation = async () => {
    try {
      const response = await axios.get('http://localhost:5000/recommend-offset', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setRecommendation(response.data);
      setWarning('');
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setWarning(error.response.data.msg);
        setRecommendation(null);
      } else {
        console.error('Error fetching recommendation:', error);
      }
    }
  };

  const handleSaveRecommendation = async () => {
    try {
      await axios.post('http://localhost:5000/save-recommendation', recommendation, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      alert('Recommendation saved!');
      setIsModalOpen(true);
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setWarning(error.response.data.msg);
      } else {
        console.error('Error saving recommendation:', error);
      }
    }
  };

  const handleRateRecommendation = async () => {
    try {
      await axios.post('http://localhost:5000/rate-recommendation', {
        ...recommendation,
        rating,
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      alert('Recommendation rated!');
      setIsModalOpen(false);
    } catch (error) {
      console.error('Error rating recommendation:', error);
    }
  };

  const currentMonth = new Date().toISOString().slice(0, 7); // Format: YYYY-MM
  const dataForCurrentMonth = emissions[currentMonth] || [];

  const pieData = {
    labels: dataForCurrentMonth.map(e => e.category),
    datasets: [{
      data: dataForCurrentMonth.map(e => e.emission),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
    }],
  };

  return (
    <Container className="dashboard">
      <Row>
        <Col xs={12} md={6} className="order-md-1 chart-container">
          <Pie data={pieData} />
        </Col>
        <Col xs={12} md={6} className="order-md-2 emission-summary">
          <p><strong>Total Emission:</strong> {totalEmission.toFixed(2)} kg CO2</p>
          <p><strong>Maximum Emission Category:</strong> {maxEmissionCategory}</p>
          {warning && <p className="warning">{warning}</p>}
          <Button color="primary" onClick={fetchRecommendation}>Get Carbon Offset Recommendation</Button>
          {recommendation && (
            <div className="mt-4">
              <h3>Recommendation</h3>
              <p>Project: {recommendation.project}</p>
              <p>Category: {recommendation.category}</p>
              <p>Description: {recommendation.description}</p>
              <Button color="success" onClick={handleSaveRecommendation}>Apply Recommendation</Button>
            </div>
          )}
        </Col>
      </Row>
      <Modal isOpen={isModalOpen} toggle={() => setIsModalOpen(!isModalOpen)}>
        <ModalHeader toggle={() => setIsModalOpen(!isModalOpen)}>Rate Recommendation</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="rating">Rating</Label>
              <Input
                type="number"
                id="rating"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
                placeholder="Rating"
                min="1"
                max="5"
                required
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={handleRateRecommendation}>Submit Rating</Button>
        </ModalFooter>
      </Modal>
    </Container>
  );
};

export default Dashboard;
