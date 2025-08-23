// Styling Imports
import { Container, Content, Banner } from "./styles.js";

// Theme Swap Imports
import { ThemeProvider } from 'styled-components';

import GlobalStyles from '../../styles/global'
import darkTheme from '../../styles/theme';

// Components Imports
import { Header } from "../../components/Header";
import { Card } from "../../components/Card";

// Strategic Imports (API and others)
import { api } from '../../services/api';
import { useState, useEffect } from 'react';

// Swiper Import
import { Swiper, SwiperSlide } from "swiper/react";

// Swiper style Import
import "swiper/css";
import "swiper/css/navigation";

// Swiper Required Module
import { Navigation } from "swiper";

export function Home() {
    const themeMode = darkTheme

    const [dishes, setDishes] = useState([])
    const [search, setSearch] = useState("")

    useEffect(() => {
        async function fetchDishes() {
          const response = await api.get(`/dishes?title=${search}`);
          setDishes(response.data);
    }
    fetchDishes();
    }, [search])

    return(
        <ThemeProvider theme={themeMode}>
            <GlobalStyles />
                <Container>
                    <Header/>
                        <Content>

                            <div className="cards">   
                                <p>Pratos executivos</p>

                                {
                                    dishes.filter(dish => dish.category == "dishes").length > 0 &&
                                        <Swiper
                                            grabCursor={true}
                                            loop={true}
                                            loopFillGroupWithBlank={true}
                                            breakpoints={{
                                                "@0.00": {
                                                    slidesPerView: 1,
                                                    spaceBetween: 10,
                                                },
                                                "@0.75": {
                                                    slidesPerView: 2,
                                                    spaceBetween: 20,
                                                },
                                                "@1.00": {
                                                    slidesPerView: 3,
                                                    spaceBetween: 40,
                                                },
                                                "@1.20": {
                                                    slidesPerView: 4,
                                                    spaceBetween: 160,
                                                },
                                            }}
                                            navigation={true}
                                            modules={[Navigation]}
                                            className="mySwiper"
                                        >
                                            {
                                                dishes.filter(dish => dish.category == "dishes").map((item, index) => (
                                                    <SwiperSlide
                                                        key={String(index)}
                                                    >
                                                        <Card 
                                                            data={item}
                                                        />
                                                    </SwiperSlide>
                                                ))
                                            }
                                        </Swiper>
                                }
                            </div>
                        </Content>
                </Container>
        </ThemeProvider>
    );
}