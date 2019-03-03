import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';
import Webcam from 'react-webcam';
import { Link } from 'react-router-dom';

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


  render() {
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
          <TextField label="Name" variant="outlined" style={textFieldStyle}/>
          <TextField label="Venmo Id" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 1 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 2 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 3 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 4 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 5 email" variant="outlined" style={{...textFieldStyle, marginBottom: 20}}/>
        </FormGroup>
        <Link to="/dashboard">
          <Button
            variant="contained"
            color="primary"
            size="large"
          >
          Next
          </Button>
        </Link>
      </div>
    );
  }
}

export default NewReceipt;