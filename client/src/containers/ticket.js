import React,{Component} from 'react';
import {Field,reduxForm} from 'redux-form';
import {renderInput,renderRadio} from '../utils/redux-form-fields';
import {connect} from 'react-redux';
  import {submitTicket} from '../actions';
import Nav from './nav.js';

class Ticket extends Component {
  formSubmit(formValue){
    formValue['seatclass']=this.props.class.seatClass;
    formValue['date_of_journey']=this.props.match.params.doj;
    formValue['boarding_station']=this.props.match.params.source;
    this.props.submitTicket(formValue,this.props.match.params.id,()=>{
      this.props.history.push('/mybookings');
    });
  }
  render(){
    //const {train} = this.props.seats.seats;
    const {handleSubmit} = this.props;
    return (
      <div className="container">
        <div className="columns content">
          <div className="column col-5 centered">
            <div className="panel">
              <Nav id={this.props.match.params.id}/>
              <form onSubmit={handleSubmit(this.formSubmit.bind(this))}>
                <div className="panel-body">
                  <div className="columns">
                      <div className="column col-6">
                        <Field component={renderInput} type="text" name="passenger_first_name" label="First Name" placeholder="First Name"/>
                      </div>
                      <div className="column col-6">
                        <Field component={renderInput} type="text" name="passenger_last_name" label="Last Name" placeholder="Last Name"/>
                      </div>
                      <div className="column col-12">
                        <div className="form-group">
                          <label className="form-label">Train no</label>
                          <input className="form-input" type="text" id="input-example-1" value={this.props.match.params.id} disabled/>
                        </div>
                      </div>
                      <div className="column col-6">
                          <Field component={renderInput} type="text" name="passenger_age" label="Age" placeholder="Age"/>
                      </div>
                      <div className="column col-6">
                        <div className="form-group float-right">
                          <label className="form-label">Gender</label>
                          <label className="form-radio">
                            <Field component="input" type="radio" name="passenger_gender" value="M"/>
                            <i className="form-icon"></i> Male
                          </label>
                          <label className="form-radio">
                            <Field component="input" type="radio" name="passenger_gender" value="F"/>
                            <i className="form-icon"></i> Female
                          </label>
                        </div>
                      </div>
                      <div className="column col-12">
                        <div className="form-group">
                          <label className="form-label">Journey Date</label>
                          <input className="form-input" type="text" name="date_of_journey" value={this.props.match.params.doj} disabled/>
                        </div>
                      </div>
                      <div className="column col-12">
                          <div className="form-group">
                            <label className="form-label">Boarding Station</label>
                            <input className="form-input" type="text" name="boarding_station" value={this.props.match.params.source} disabled/>
                          </div>
                      </div>
                  </div>
                </div>
                <div className="panel-footer">
                  <div className="form-group">
                    <input className="btn btn-success btn-lg btn-block" type="submit"/>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

Ticket = reduxForm({
	form:'TicketForm',
	fields:['passenger_first_name','passenger_last_name','seatClass','passenger_age','passenger_gender', 'boarding_station']
})(Ticket);

function mapStateToProps(state){
  return {
    class:state.class,
  }
}

export default connect(mapStateToProps,{submitTicket})(Ticket);
