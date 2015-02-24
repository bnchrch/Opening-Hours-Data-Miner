
module.exports = function(sequelize, DataTypes) {
    var Place = sequelize.define('Place', {
        is_active: {
            type: DataTypes.BOOLEAN,
            defaultValue: true,
            allowNull: false
        },
        expires_at: DataTypes.DATE,
        message: DataTypes.STRING,
        image_1: {
            type: DataTypes.STRING,
            allowNull: false
        },
        image_2: {
            type: DataTypes.STRING,
            allowNull: false
        },
        vote_count_1: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
            allowNull: false
        },
        vote_count_2: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
            allowNull: false
        }


    }, {
        classMethods: {
            associate: function(models) {
                Place.belongsTo(models.apiCall);
                ThisThat.hasMany(models.Vote, {onDelete: 'cascade'});
            }

        },
        instanceMethods: {
            hasUser: function(user) {
                if (user.id === this.userId) {
                    return true;
                }
                else return false
            }
        },
        tableName: 'thisthat'
    });



    return Place
}
