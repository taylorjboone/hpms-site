import React from 'react';
import { Formik } from 'formik';

export const Basic2 = () => {
    return <div>
        <h1>Anywhere in your app!</h1>
        <Formik
            initialValues={{ id: '', route_id: '', bmp: '', emp: '', }}
        >
        </Formik>
    </div>
}

export default Basic2;