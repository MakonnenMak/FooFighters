import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';
import Webcam from 'react-webcam';
import { Redirect } from 'react-router';
import axios from 'axios';

const textFieldStyle = {
  width: 500,
  margin: "0 auto",
  marginTop: 20
};

const videoConstraints = {
      width: 1280,
      height: 720,
};


class NewReceipt extends Component {
  setRef = webcam => {
    this.webcam = webcam;
  };

  constructor(props) {
    super(props);
    this.state = {
      image_source: "",
      imageTaken: false,
      venmo: "",
      recepient1: "",
      recepient2: "",
      recepient3: "",
      recepient4: "",
      recepient5: "",
      navigate: false,
    };
  }

  capture = () => {
    const imageSrc = this.webcam.getScreenshot();
    this.setState({
      image_source: imageSrc,
      imageTaken: true,
    });
  };

  recapture = () => {
    this.setState({
      image_source: "",
      imageTaken: false,
    })
  }

  handleButtonClick = () => {
    if (this.state.imageTaken) {
        let recepients = []
        if (this.state.recepients1) {
          recepients.push(this.state.recepients1);
        }
        if (this.state.recepients2) {
          recepients.push(this.state.recepients2);
        }
        if (this.state.recepients3) {
          recepients.push(this.state.recepients3);
        }
        if (this.state.recepients4) {
          recepients.push(this.state.recepients4);
        }
        if (this.state.recepients5) {
          recepients.push(this.state.recepients5);
        }
        recepients.push(this.props.rootState.userEmail);

      let data = {
        recepients: recepients,
        venmo_id: this.state.venmo,
        img_url: this.state.image_source,
      };
      console.log(data)
      axios.post("http://localhost:8000/apilayer/senddata/" + this.props.rootState.userEmail, data)
      .then(res => {
        console.log(res);
        console.log(res.data);
        this.setState({
          ...this.state,
          navigate: true
        });
      });
    }
  }


  render() {
    if (this.state.navigate) {
      return <Redirect to="/dashboard" push={true}/>
    }
    let image, clickFunc;
    if (this.state.imageTaken) {
      image =
        <img
          src={this.state.image_source} 
          alt="camera"
          style={
            {
              margin: "0 auto",
              marginTop: 60,
              marginBottom: 60,
            }}
        />;
        clickFunc = this.recapture;
    } else {
      image = 
        <Webcam
          audio={false}
          ref={this.setRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
        />;
        clickFunc = this.capture;

    }

    return (
      <div>
        <Typography component="h2" variant="h2">New Receipt</Typography>
        { image }
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={clickFunc}
          style={{
            display: "block",
            margin: "0 auto"
          }}
        >
        {this.state.imageTaken ? "Recapture": "Capture"}
        </Button>
        <FormGroup>
          <TextField label="Venmo Id" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, venmo: event.target.value})} value={this.state.venmo}/>
          <TextField label="Recepient 1 email" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, recepient1: event.target.value})} value={this.state.recepient1}/>
          <TextField label="Recepient 2 email" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, recepient2: event.target.value})} value={this.state.recepient2}/>
          <TextField label="Recepient 3 email" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, recepient3: event.target.value})} value={this.state.recepient3}/>
          <TextField label="Recepient 4 email" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, recepient4: event.target.value})} value={this.state.recepient4}/>
          <TextField label="Recepient 5 email" variant="outlined" style={textFieldStyle} onChange={(event) => this.setState({...this.state, recepient5: event.target.value})} value={this.state.recepient5}/>
        </FormGroup>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={this.handleButtonClick}
          >
          Submit
          </Button>
      </div>
    );
  }
}

export default NewReceipt;