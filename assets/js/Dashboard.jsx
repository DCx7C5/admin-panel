import React, { Component } from 'react';
import '../css/Dashboard.css';


class Dashboard extends Component {
  constructor(props) {
    super(props);

    // Initialize state to store the current time
    this.state = {
      currentTime: new Date().toLocaleTimeString(),
    };
  }

  componentDidMount() {
    // Update the time every second
    this.intervalID = setInterval(() => {
      this.setState({
        currentTime: new Date().toLocaleTimeString(),
      });
    }, 1000);
  }

  componentWillUnmount() {
    // Clear the interval to stop updating the time when the component is unmounted
    clearInterval(this.intervalID);
  }

  render() {
    return (
      <div>
        <h1>Realtime Clock</h1>
        <p>{this.state.currentTime}</p>
      </div>
    );
  }
}

export default Dashboard;