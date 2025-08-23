// Styling Imports
import { Container, Content, Form, Image } from "./styles.js";

// Theme Swap Imports
import { ThemeProvider } from 'styled-components';

import GlobalStyles from '../../styles/global'

import darkTheme from '../../styles/theme';

// Components Imports
import { Header } from "../../components/Header";
import { Button } from "../../components/Button";
import { ButtonText } from "../../components/ButtonText";
import { Input } from "../../components/Input";
import { Textarea } from "../../components/Textarea";
import { PageError } from "../../components/PageError";

// Strategic Imports (API and others)
import { api } from "../../services/api";
import { useAuth } from "../../hooks/auth";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";

// Image Imports
import { RiArrowLeftSLine } from 'react-icons/ri';
import { FiCamera } from "react-icons/fi";

export function EditDish() {
    const themeMode = darkTheme;
    const navigate = useNavigate();
    
    const { user } = useAuth()
    const params = useParams();

    const [loading, setLoading] = useState(false);
    const [loadingDelete, setLoadingDelete] = useState(false);
    
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("");

    
    const [data, setData] = useState(null);
    
    // Change Image Function
    const imageURL = data && `${api.defaults.baseURL}/files/${data.image}`;
    const [image, setImage] = useState();
    const [imageFile, setImageFile] = useState(null)

    function handleChangeImage(event) {
        const file = event.target.files[0];
        setImageFile(file);

        const imagePreview = URL.createObjectURL(file);
        setImage(imagePreview);
    }

    // Update Dish Function
    async function handleUpdateDish() {
        if (!image) {
            return alert("Erro: Você não carregou a nova imagem do prato!");
        }
        
        if (!title) {
            return alert("Erro: Você não informou o nome do prato!");
        }

        if (!category) {
            return alert("Erro: Você não selecionou a categoria do prato!");
        }

        if (!price) {
            return alert("Erro: Você não informou o preço do prato!");
        }

        if (!description) {
            return alert("Erro: Você não informou uma descrição para o prato!");
        }

        setLoading(true);

        const formData = new FormData();
        formData.append("image", imageFile);
        formData.append("title", title);
        formData.append("description", description);
        formData.append("category", category);
        formData.append("price", price);

        await api
            .put(`/dishes/${params.id}`, formData)
            .then(alert("Prato atualizado com sucesso!"), navigate("/"))
            .catch((error) => {
                if (error.response) {
                    alert(error.response.data.message);
                } else {
                    alert("Erro ao atualizar o prato!");
                }
            });  
        
        setLoading(false);
    }

    useEffect(() => {
        async function fetchDish() {
            const response = await api.get(`/dishes/${params.id}`);
            setData(response.data);
            
            const { title, description, category, price } = response.data;
            setTitle(title);
            setDescription(description);
            setCategory(category);
            setPrice(price);
        }
    
        fetchDish();
    }, [])

    // Remove Dish Function
    async function handleRemoveDish() {
        setLoadingDelete(true);
        const isConfirm = confirm("Tem certeza que deseja remover este item?");
    
        if(isConfirm) {
            await api.delete(`/dishes/${params.id}`)
            .then(() => {
                alert("Item removido com sucesso!");
                navigate("/");
                setLoadingDelete(false);
            })
        } else {
            return
        }
    }
      
    return(
        <ThemeProvider theme={themeMode}>
            <GlobalStyles />
                <Container>
                    <Header />

                    {
                        user.isAdmin ?

                            <Content>

                            {
                                data &&

                                <Form>
                                    <header>
                                        <Link to="/">
                                            <ButtonText title="Voltar" icon={RiArrowLeftSLine}/>
                                        </Link>
                                        <h1>Editar prato</h1>
                                    </header>

                                    <div className="details">
                                        <div className="dishImage">
                                            <p>Imagem do Prato</p>

                                            <Image>
                                                <img 
                                                    src={image ? image : imageURL} 
                                                    alt="Foto do prato" 
                                                />

                                                <label htmlFor="image">
                                                    <FiCamera />

                                                    <input
                                                        id="image"
                                                        type="file"
                                                        name="image"
                                                        accept="image/*"
                                                        onChange={handleChangeImage}
                                                    />
                                                </label>
                                            </Image>
                                        </div>

                                        <div className="dishDetails">
                                            <div className="dishName">
                                                <div className="dish">
                                                    <p>Nome do prato</p>
                                                    <Input
                                                        placeholder="Ex.: Salada Caesar"
                                                        type="text"
                                                        value={title}
                                                        onChange={e => setTitle(e.target.value)}
                                                    />
                                                </div>
                                            </div>

                                            <div className="dishIngredients">

                                                <div className="price">
                                                    <p>Preço</p>
                                                    <Input
                                                        placeholder="R$ 00,00"
                                                        type="number"
                                                        value={price} 
                                                        onChange={e => setPrice(e.target.value)}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="textarea">
                                        <p>Descrição</p>
                                        <Textarea 
                                            placeholder="Fale brevemente sobre o prato, seus ingredientes e composição"
                                            defaultValue={description} 
                                            onChange={e => setDescription(e.target.value)}
                                        />
                                    </div>

                                </Form>
                                }

                            <div className="button">
                                <Button 
                                    className="deleteButton"
                                    title={loadingDelete ? "Excluindo prato" : "Excluir prato"}
                                    onClick={handleRemoveDish}
                                    disabled={loadingDelete} 
                                />
                                <Button 
                                    title={loading ? "Salvando alterações" : "Salvar alterações"}
                                    onClick={handleUpdateDish}
                                    disabled={loading} 
                                />
                            </div>

                            </Content>

                        :

                            <PageError />
                    }
                </Container>
        </ThemeProvider>
    );
}