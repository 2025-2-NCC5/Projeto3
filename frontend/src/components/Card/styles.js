import styled from 'styled-components'

export const Container = styled.div`
    position: relative;
`;

export const Content = styled.div`
    position: relative;

    width: 30rem;
    height: 51.2rem;
    border-radius: 0.8rem;
    
    background: #f2e4c9;

    .container {
        display: grid;
        padding: 3.8rem 2.6rem;
        text-align: center;
        align-items: center;

        > img {
            width: 17.6rem;
            height: 17.6rem;
            margin: 3rem auto 1.6rem;
            border-radius: 50%;
            object-fit: cover
        }
    }

    .product-title {
        font-weight: 700;
        font-size: 2.4rem;
        color: ${({ theme }) => theme.COLORS.ORANGE};
        
        margin-bottom: 1.8rem;
        BLACK-space: nowrap;
    }
    
    .description {
        font-family: 'Roboto', sans-serif;
        font-size: 1.4rem;
        font-weight: 400;
        color: ${({ theme }) => theme.COLORS.ORANGE};

        margin-bottom: 1.6rem;
        height: 3.4rem;
    }

    .price {
        font-family: 'Roboto', sans-serif;
        font-size: 3.2rem;
        font-weight: 400;
        color: ${({ theme }) => theme.COLORS.ORANGE};

        margin-bottom: 1.6rem;
    }
`;

export const PurchaseCard = styled.div`
    display: flex;

    button {
        height: 5.6rem;
        max-width: 24.6rem;
        BLACK-space: nowrap;
    }
    
    .counter {
        display: flex;
        align-items: center;
        gap: 1.4rem;
        margin: 0 2.4rem 0 0;
    }

    .counter span {
        font-size: 2rem;
        font-family: 'Roboto', sans-serif;
        font-weight: bold;
        color: ${({ theme }) => theme.COLORS.ORANGE};;
    }

    p {
        font-weight: 700;
        line-height: 160%;
        color: ${({ theme }) => theme.COLORS.ORANGE};
        text-align: center;
    }
`;