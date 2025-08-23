// Styling Imports
import { Container, Form, Logo } from "./styles";

// Theme Import
import { ThemeProvider } from 'styled-components';
import GlobalStyles from '../../styles/global'
import darkTheme from '../../styles/theme';

// Components Imports
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";

// Strategic Imports (API and others)
import { useAuth } from "../../hooks/auth";
import { useState } from "react";
import { Link } from "react-router-dom";

export function SignIn() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    const { signIn, loading } = useAuth();
    
    function handleSignIn() {
        signIn({ email, password });
    }

    return (
        <ThemeProvider theme={darkTheme}>
            <GlobalStyles />
                <Container>
                    
                    <Logo>
                        <div className="logo">
                            <h1>Cannoli</h1>
                        </div>
                    </Logo>
                    
                    <Form>
                        <h2>Faça login</h2>

                        <div className="inputs">
                            <p>Email</p>
                            <Input
                                placeholder="Exemplo: exemplo@exemplo.com.br"
                                type="text"
                                onChange={e => setEmail(e.target.value)}
                            />
                        </div>
                        
                        <div className="inputs">
                            <p>Senha</p>
                            <Input
                                placeholder="No mínimo 6 caracteres"
                                type="password"
                                onChange={e => setPassword(e.target.value)}
                            />
                        </div>

                        <Button 
                            title={loading ? "Entrando" : "Entrar"}
                            onClick={handleSignIn} 
                            disabled={loading}
                        />

                        <Link to="/register">
                            Criar conta
                        </Link>

                    </Form>
                </Container>
        </ThemeProvider>
    );
}
