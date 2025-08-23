import React from 'react';
import ReactDOM from 'react-dom/client';

import { AuthProvider } from './hooks/auth';
import { CartProvider } from './hooks/cart';

import { Routes } from './routes';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AuthProvider>
        <CartProvider>
                <Routes />
        </CartProvider>
        </AuthProvider>
    </React.StrictMode>
)