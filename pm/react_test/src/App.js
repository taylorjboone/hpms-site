// Render Prop
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';

const Basic = () => (
  <div>
    <h1>Task Information</h1>
    <Formik
      initialValues={{ id: '',
                      route_id: '',
                      bmp: '',
                      emp: '',
                      org_num: '',
                      project_name: '',
                      activity_code: '',
                      activity_description: '',
                      route_name: '',
                      accomplishments: '',
                      units: '',
                      crew_members: '',
                      travel_hours: '',
                      onsite_hours: '',
                      task_date: '',
                      notes: '' }}
      validate={values => {
        const errors = {};
        if (!values.route_id) {
          errors.route_id = 'Required';
      } else if (( values.route_id.length != 13 ) && (values.route_id.length != 18)) {
          errors.route_id = 'Route ID must be 13 or 18 characters in length'
      }
      return errors;
  }}
  onSubmit={(values, { setSubmitting }) => {
      setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          setSubmitting(false);
      }, 400);
  }}
    >
      {({ isSubmitting }) => (
        <Form>
          <label for="id">ID</label>
          <Field type="text" name="id"/>
          <ErrorMessage name="id" component="div" />
          <br/>
          <label for="route_id">Route ID</label>
          <Field type="" name="route_id" />
          <ErrorMessage name="route_id" component="div" />
          <br/>
          <label for="bmp">BMP</label>
          <Field type="" name="bmp" />
          <ErrorMessage name="bmp" component="div" />
          <br/>
          <label for="emp">EMP</label>
          <Field type="" name="emp" />
          <ErrorMessage name="emp" component="div" />
          <br/>
          <label for="org_num">Organization Number</label>
          <Field type="" name="org_num" />
          <ErrorMessage name="org_num" component="div" />
          <br/>
          <label for="project_name">Project Name</label>
          <Field type="" name="project_name" />
          <ErrorMessage name="project_name" component="div" />
          <br/>
          <label for="activity_code">Activity Code</label>
          <Field type="" name="activity_code" />
          <ErrorMessage name="activity_code" component="div" />
          <br/>
          <label for="activity_description">Activity Description</label>
          <Field type="" name="activity_description" />
          <ErrorMessage name="activity_description" component="div" />
          <br/>
          <label for="route_name">Route Name</label>
          <Field type="" name="route_name" />
          <ErrorMessage name="route_name" component="div" />
          <br/>
          <label for="accomplishments">Accomplishments</label>
          <Field type="" name="accomplishments" />
          <ErrorMessage name="accomplishments" component="div" />
          <br/>
          <label for="units">Units</label>
          <Field type="" name="units" />
          <ErrorMessage name="units" component="div" />
          <br/>
          <label for="crew_members">Crew Members</label>
          <Field type="" name="crew_members" />
          <ErrorMessage name="crew_members" component="div" />
          <br/>
          <label for="travel_hours">Travel Hours</label>
          <Field type="" name="travel_hours" />
          <ErrorMessage name="travel_hours" component="div" />
          <br/>
          <label for="onsite_hours">On-Site Hours</label>
          <Field type="" name="onsite_hours" />
          <ErrorMessage name="onsite_hours" component="div" />
          <br/>
          <label for="task_date">Task Date</label>
          <Field type="" name="task_date" />
          <ErrorMessage name="task_date" component="div" />
          <br/>
          <label for="notes">Notes</label>
          <Field type="" name="notes" />
          <ErrorMessage name="notes" component="div" />
          <br/>
          
          <button type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </Form>
      )}
    </Formik>
  </div>
);

export default Basic;