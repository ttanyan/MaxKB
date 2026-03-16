BEGIN;

CREATE TABLE "user_menu_setting" (
    "create_time" timestamp with time zone NOT NULL,
    "update_time" timestamp with time zone NOT NULL,
    "id" uuid NOT NULL PRIMARY KEY,
    "menu_list" varchar(128)[] NOT NULL,
    "user_id" uuid NOT NULL UNIQUE
);

ALTER TABLE "user_menu_setting"
    ADD CONSTRAINT "user_menu_setting_user_id_2617308f_fk_user_id"
    FOREIGN KEY ("user_id") REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "user_menu_setting_create_time_c34ef3bd"
    ON "user_menu_setting" ("create_time");

CREATE INDEX "user_menu_setting_update_time_fa3c503c"
    ON "user_menu_setting" ("update_time");

COMMIT;
