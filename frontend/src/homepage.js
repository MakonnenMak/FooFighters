// import React, { Component } from 'react';
//import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

// class Homepage extends Component {
//   render() {
//     return (
//       <div>
//         <Button
//           variant="contained"
//           color="primary"
//           size="large"
//           style={{height: 100}, {fontSize: '40px'}}
//         >
//         Create New Receipt
//         </Button>
//       </div>
//     )
//   }
// }

// export default Homepage;

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import { spacing } from '@material-ui/system';

const styles = theme => ({
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(12, 1fr)',
    gridGap: `${theme.spacing.unit * 5}px`,
  },
  paper: {
    padding: theme.spacing.unit,
    textAlign: 'center',
    color: theme.palette.text.secondary,
    whiteSpace: 'nowrap',
    marginBottom: theme.spacing.unit,
  },
  divider: {
    margin: `${theme.spacing.unit * 2}px 0`,
  },
});

function CSSGrid(props) {
  const { classes } = props;

  return (

    <div>

      <div>
        <div>
          <p>  </p>
        </div>
        <Button
          variant="contained"
          color="primary"
          size="large"
          style={{height: 50}, {fontSize: '40px'}}
        >
        Create New Receipt
        </Button>
      </div>
        <Divider className={classes.divider} />

      <div className={classes.container}>
        <div style={{  gridColumnStart: '1', gridColumnEnd: 'span 4' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt1<p>Kroger</p><p>Date</p></Paper>
        </div>
        <div style={{ gridColumnEnd: 'span 4'}}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt2<p>Kroger</p><p>Date</p></Paper>
        </div>
        <div style={{ gridColumnEnd: 'span 4' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt3<p>Kroger</p><p>Date</p></Paper>
        </div>
        <div style={{ gridColumnStart: '1', gridColumnEnd: 'span 4' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt4<p>Kroger</p><p>Date</p></Paper>
        </div>
        <div style={{ gridColumnEnd: 'span 4' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt5<p>Kroger</p><p>Date</p></Paper>
        </div>
        <div style={{ gridColumnEnd: 'span 4' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>receipt6<p>Kroger</p><p>Date</p></Paper>
        </div>
      </div>
    </div>
  );
}

CSSGrid.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CSSGrid);
