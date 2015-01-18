var game = game || {
    Collection: {},
    Model: {},
    View: {}
}
game.Collection = Backbone.Collection.extend({
    model: game.Model
});
game.Model = Backbone.Model.extend({
    initialize: function() {
    }
});
game.View = Backbone.View.extend({
    tagName: "div",
    className: "game-root",
    initialize: function() {
    },
    render: function() {
    }
});