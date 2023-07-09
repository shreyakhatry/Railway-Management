import React,{Component} from 'react';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';

class Trains extends Component {
  renderEachTrain(train){
    return (
      <div className="column col-11" key={train.id}>
        <div className="panel panel-pad">
          <div className="panel-header">
            <div className="panel-title">{train.train_name}-{train.train_number}</div>
          </div>

          <div className="panel-footer">
            <div className="columns">
              <div className="column col-4">
                <a className="btn btn-link btn-lg"><i className="icon icon-time"></i> Arrival - {train.arrival}</a>
              </div>
              <div className="column col-4">
                <a className="btn btn-link btn-lg"><i className="icon icon-time"></i> Departure- {train.departure}</a>
              </div>
            </div>
            <div className="columns">
            <div className="column col-4">
                  <Link className="btn btn-default btn-lg" to={`ticket/${train.id}/${train.number}/${this.props.doj.date}`}>Book Now</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
  render(){
    const trains = this.props.data.trains;
    return(
      <div className="columns">
        {trains.map(this.renderEachTrain.bind(this))}
      </div>
    )
  }
}

function mapStateToProps(state){
  return {
    doj:state.doj
  }
}
export default connect(mapStateToProps)(Trains);