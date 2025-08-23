import styled from "styled-components";

export const Container = styled.div`
    display: flex;
    flex-direction: column;
    
    width: 100%;
    min-width: 35rem;
    height: 100vh;
    
    overflow: auto;
    overflow: overlay; 
`;

export const Content = styled.div`
    display: flex;
    flex-direction: column;
    
    width: 100%;
    max-width: 121.2rem;
    margin: auto;
    padding: 3.5rem 4rem;

    font-family: 'Poppins', sans-serif;

    .swiper {
        margin-bottom: 6rem;
    }

    p {
        font-size: 3.2rem;
        margin-bottom: 3rem;
        color: black;
    }
    
    .swiper-slide {
        /* Center slide text vertically */
        display: -webkit-box;
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
        -webkit-box-align: center;
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
    }
    
    .swiper-button-next,
    .swiper-button-prev {
        width: 9rem;
        height: 51.2rem;
        margin: -25.6rem -1rem;
        
        color: ${({ theme }) => theme.COLORS.BLACK};
        font-weight: bolder;
        mask-image: none;
    }

    .swiper-button-next:hover,
    .swiper-button-prev:hover {
	    animation: scale-up-center 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
    }

    .swiper-button-prev {
        background: linear-gradient(to left, transparent 0%, ${({ theme }) => theme.COLORS.BLACK} 100% 0%, transparent 100%);
    }

    .swiper-button-next {
        background: linear-gradient(to right, transparent 0%, ${({ theme }) => theme.COLORS.BLACK} 100% 0%, transparent 100%);
    }

    @keyframes scale-up-center {
        0% {
            transform: scale(1);
        }
        100% {
            transform: scale(1.2);
        }
    }
`;

export const Banner = styled.div`
    
`;
