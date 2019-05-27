from orator.migrations import Migration


class CreateImagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("images") as t:
            t.increments("id")
            t.integer("article_id").unsigned()
            t.string("original_url")
            t.string("path")
            # t.string("thumb_url") # 以后会用到，目前先把缩略图存到 mysql，以后要放到对象存储
            t.timestamps()

            t.index(["article_id", "original_url"])
            t.index(['original_url'])
            t.index("updated_at")


        with self.schema.table("articles") as t:
            t.integer("images_num").default(-1)


    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("images")
        with self.schema.table("articles") as t:
            t.drop_column("images_num")
