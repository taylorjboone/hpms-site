import React from 'react';
import { Formik } from 'formik';

const Basic = () => (
  <div>
    <h1>Anywhere in your app!</h1>
    <Formik
      initialValues={{ email: '', password: '' }}
      validate={values => {
        const errors = {};
        if (!values.email) {
          errors.email = 'Required';
        } else if (
          !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
        ) {
          errors.email = 'Invalid email address';
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
      {({
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        handleSubmit,
        isSubmitting,
        /* and other goodies */
      }) => (
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            onChange={handleChange}
            onBlur={handleBlur}
            value={values.email}
          />
          {errors.email && touched.email && errors.email}
          <input
            type="password"
            name="password"
            onChange={handleChange}
            onBlur={handleBlur}
            value={values.password}
          />
          {errors.password && touched.password && errors.password}
          <button type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </form>
      )}
    </Formik>
  </div>
);

export default Basic;

import React from 'react';
import { Formik } from 'formik';

export const Basic2 = () => {
    return <div>
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
            {({
                values,
                errors,
                touched,
                handleChange,
                handleBlur,
                handleSubmit,
                isSubmitting,
                /* and other goodies */
            }) => (
                <form onSubmit={handleSubmit}>
                    <input
                        type=""
                        name=""
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.}
                    />
                    {errors. && touched.}
                    <input
                        type=""
                        name=""
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.}
                    />
                    {errors. && touched.}
                    
                    <button type="submit" disabled={isSubmitting}>
                        Submit
                    </button>
                </form>
            )}
        </Formik>
    </div>
};

export default Basic2;
