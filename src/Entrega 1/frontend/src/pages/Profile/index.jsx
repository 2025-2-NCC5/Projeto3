// Styling Imports
import { Container, Content, Form, Infos} from './styles';

// Theme Swap Imports
import { ThemeProvider } from 'styled-components';

import GlobalStyles from '../../styles/global'

import darkTheme from '../../styles/theme';

// Components Imports
import { Header } from '../../components/Header';
import { Button } from '../../components/Button';

// Strategic Imports (API and others)
import { api } from '../../services/api';
import { useAuth } from '../../hooks/auth';
import { useState } from 'react';
import { Link } from "react-router-dom";

// Image Imports
import { FiUser, FiMail, FiLock, FiCamera, FiShoppingBag, FiPlus } from 'react-icons/fi';
import { BsWhatsapp } from 'react-icons/bs';
import avatarPlaceholder from '../../assets/avatar_placeholder.svg';

export function Profile() {
    const themeMode = darkTheme

    const { user, updateProfile, loading } = useAuth();

    const [name, setName] = useState(user.name);
    const [email, setEmail] = useState(user.email);
    const [passwordOld, setPasswordOld] = useState();
    const [passwordNew, setPasswordNew] = useState();

    // Update User Function

    async function handleUpdate() {
        const updated = {
            name,
            email,
            password: passwordNew,
            old_password: passwordOld,
        }

        const userUpdated = Object.assign(user, updated);

        await updateProfile({ user: userUpdated });
    }


    return (
        <ThemeProvider theme={themeMode}>
            <GlobalStyles />
                <Container>
                    <Header />
                        <Content>

                            <div className='card'>
                                <Form>
                                    <div className='inputs'>
                                        <label>
                                            <FiUser size={20}/>
                                            <input 
                                                type="text" 
                                                placeholder="Nome"
                                                value={name}
                                                onChange={e => setName(e.target.value)}
                                            />
                                        </label>

                                        <label>
                                            <FiMail size={20}/>
                                            <input 
                                                type="text" 
                                                placeholder="E-mail"
                                                value={email}
                                                onChange={e => setEmail(e.target.value)}
                                            />
                                        </label>

                                        <label>
                                            <FiLock size={20}/>
                                            <input 
                                                type="password" 
                                                placeholder="Senha atual"
                                                onChange={e => setPasswordOld(e.target.value)}
                                            />
                                        </label>

                                        <label>
                                            <FiLock size={20}/>
                                            <input 
                                                type="password" 
                                                placeholder="Nova senha"
                                                onChange={e => setPasswordNew(e.target.value)}
                                            />
                                        </label>
                                    </div>

                                    <Button 
                                        title={loading ? "Salvando" : "Salvar"}
                                        onClick={handleUpdate} 
                                        disabled={loading}
                                    />
                                </Form>

                                {
                                    user.isAdmin ?

                                        <Infos>
                                            <p>Olá <span>{name}</span>, acesse a opção desejada:</p>

                                            <Link to="/orders">
                                                <Button
                                                    title="Ver pedidos"
                                                    icon={FiShoppingBag}
                                                />
                                            </Link>

                                            <Link to="/createdish">
                                                <Button 
                                                    title="Criar novo Prato"
                                                    icon={FiPlus}
                                                />
                                            </Link>
                                        </Infos>

                                    :

                                        <Infos>
                                            <p>Olá <span>{name}</span>, acesse a opção desejada:</p>

                                            <Link to="/orders">
                                                <Button
                                                    title="Meus pedidos"
                                                    icon={FiShoppingBag}
                                                />
                                            </Link>
                                        </Infos>
                                }
                            </div>
                        </Content>
                </Container>
        </ThemeProvider>
    );
}