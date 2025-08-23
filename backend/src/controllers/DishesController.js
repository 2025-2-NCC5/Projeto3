// Knex, App Error and Disk Storage Import
const knex = require("../database/knex");
const AppError = require('../utils/AppError');
const DiskStorage = require("../providers/DiskStorage")

class DishesController {
    async create(request, response) {
        const { title, description, category, price } = request.body;

        const checkDishAlreadyExists = await knex("dishes").where({ title }).first();
    
        if (checkDishAlreadyExists) {
            throw new AppError("Este prato já existe no cardápio.");
        }

        const imageFileName = request.file.filename;
        const diskStorage = new DiskStorage();
        const filename = await diskStorage.saveFile(imageFileName);

        await knex("dishes").insert({
            image: filename,
            title,
            description,
            price,
            category,
        });

        return response.status(201).json(); 
    }

    async update(request, response) {
        const { title, description, category, price } = request.body;
        const { id } = request.params;

        const imageFileName = request.file.filename;
        const diskStorage = new DiskStorage();

        const dish = await knex("dishes").where({ id }).first();

        if (dish.image) {
            await diskStorage.deleteFile(dish.image);
        }

        const filename = await diskStorage.saveFile(imageFileName);

        dish.image = filename ?? dish.image;
        dish.title = title ?? dish.title;
        dish.description = description ?? dish.description;
        dish.category = category ?? dish.category;
        dish.price = price ?? dish.price;

        await knex("dishes").where({ id }).update(dish);

        return response.status(201).json('Prato atualizado com sucesso');
    }

    async show(request, response) {
        const { id } = request.params;

        const dish = await knex("dishes").where({ id }).first();

        return response.status(201).json(dish);
    }

    async delete(request, response) {
        const { id } = request.params;

        await knex("dishes").where({ id }).delete();

        return response.status(202).json();
    }

    async index(request, response) {
        const { title } = request.query;

        const dishes = await knex("dishes")
            .whereLike("title", `%${title}%`)
            .orderBy("title");

        return response.status(200).json(dishes);
    }
}

module.exports = DishesController;