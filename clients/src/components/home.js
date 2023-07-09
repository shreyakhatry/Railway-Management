import React from 'react';

const Home = () => {
  const headingStyle = {
    color: 'black',
    fontSize: '100px',
    fontWeight: 'bold',
  };
  return (
    <div>
      <h1 style={headingStyle}>Welcome to Railway Website</h1>
      <p className="redText">Book your train tickets online.</p>
    </div>
  );
}

export default Home;
