import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import { Container, Row, Col } from 'reactstrap';
import '../EmissionHistory.css';

Chart.register(ArcElement, Tooltip, Legend);

const EmissionHistory = () => {
  const [data, setData] = useState([]);
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const recommendationsResponse = await axios.get('http://localhost:5000/recommendations', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        const emissionsResponse = await axios.get('http://localhost:5000/emissions', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        const recommendations = recommendationsResponse.data;
        const emissions = emissionsResponse.data;

        const combinedData = {};

        recommendations.forEach(rec => {
          const month = rec.date.slice(0, 7);
          if (!combinedData[month]) {
            combinedData[month] = { recommendations: [], emissions: [] };
          }
          combinedData[month].recommendations.push(rec);
        });

        Object.entries(emissions).forEach(([month, emissionsData]) => {
          if (!combinedData[month]) {
            combinedData[month] = { recommendations: [], emissions: [] };
          }
          combinedData[month].emissions = emissionsData;
        });

        setData(Object.entries(combinedData));

        const summaryData = Object.entries(emissions).map(([month, data]) => {
          const total = data.reduce((sum, e) => sum + e.emission, 0);
          const maxCategory = data.reduce((max, e) => e.emission > max.emission ? e : max, { category: '', emission: 0 });
          return {
            month,
            totalEmission: total,
            maxEmissionCategory: maxCategory.category ? `${maxCategory.category} (${maxCategory.emission.toFixed(2)} kg CO2)` : 'N/A',
          };
        });

        setSummary(summaryData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Container className="emission-history">
      <h2>Monthly Recommendations and Emissions</h2>
      {data.map(([month, { recommendations, emissions }]) => {
        const pieData = {
          labels: emissions.map(e => e.category),
          datasets: [{
            data: emissions.map(e => e.emission),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
          }],
        };

        const totalEmission = emissions.reduce((sum, e) => sum + e.emission, 0);
        const maxCategory = emissions.reduce((max, e) => e.emission > max.emission ? e : max, { category: '', emission: 0 });

        return (
          <div key={month} className="month-section">
            <h3>{month}</h3>
            <Row>
              <Col xs={12} md={6}>
                <h4>Emissions</h4>
                <div className="chart-container">
                  <Pie data={pieData} />
                </div>
                <div className="emission-summary">
                  <p><strong>Total Emission:</strong> {totalEmission.toFixed(2)} kg CO2</p>
                  <p><strong>Maximum Emission Category:</strong> {maxCategory.category ? `${maxCategory.category} (${maxCategory.emission.toFixed(2)} kg CO2)` : 'N/A'}</p>
                </div>
              </Col>
              <Col xs={12} md={6}>
                <h4>Recommendation</h4>
                {recommendations.length > 0 ? (
                  <ul>
                    {recommendations.map((rec, index) => (
                      <li key={index}>
                        <strong>Date:</strong> {rec.date}<br />
                        <strong>Project:</strong> {rec.project}<br />
                        <strong>Category:</strong> {rec.category}<br />
                        <strong>Description:</strong> {rec.description}<br />
                        {rec.project && (
                          <img src={require(`../assets/${rec.project}.png`)} alt={rec.project} className="recommendation-image" />
                        )}
                        <strong>Rating:</strong> {rec.rating || 'Not rated yet'}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No recommendations found.</p>
                )}
              </Col>
            </Row>
          </div>
        );
      })}
    </Container>
  );
};

export default EmissionHistory;
