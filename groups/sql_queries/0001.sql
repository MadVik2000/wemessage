BEGIN;

--
-- Create model Group
--
CREATE TABLE
    "groups_group" (
        "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
        "created_at" timestamp
        with
            time zone NOT NULL,
            "updated_at" timestamp
        with
            time zone NOT NULL,
            "is_active" boolean NOT NULL,
            "name" varchar(255) NOT NULL,
            "tag" varchar(32) NOT NULL UNIQUE,
            "description" text NOT NULL,
            "image" varchar(100) NULL,
            "created_by_id" uuid NULL,
            "updated_by_id" uuid NULL
    );

--
-- Create model GroupMessage
--
CREATE TABLE
    "groups_groupmessage" (
        "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
        "created_at" timestamp
        with
            time zone NOT NULL,
            "updated_at" timestamp
        with
            time zone NOT NULL,
            "is_active" boolean NOT NULL,
            "message" text NOT NULL,
            "created_by_id" uuid NULL,
            "group_id" bigint NOT NULL,
            "updated_by_id" uuid NULL
    );

--
-- Create model GroupMember
--
CREATE TABLE
    "groups_groupmember" (
        "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
        "created_at" timestamp
        with
            time zone NOT NULL,
            "updated_at" timestamp
        with
            time zone NOT NULL,
            "is_active" boolean NOT NULL,
            "admin" boolean NOT NULL,
            "created_by_id" uuid NULL,
            "group_id" bigint NOT NULL,
            "updated_by_id" uuid NULL,
            "user_id" uuid NOT NULL,
            CONSTRAINT "unique_group_user" UNIQUE ("group_id", "user_id")
    );

ALTER TABLE "groups_group" ADD CONSTRAINT "groups_group_created_by_id_498c8e85_fk_users_user_uuid" FOREIGN KEY ("created_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_group" ADD CONSTRAINT "groups_group_updated_by_id_57f18485_fk_users_user_uuid" FOREIGN KEY ("updated_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "groups_group_tag_bbb8825d_like" ON "groups_group" ("tag" varchar_pattern_ops);

CREATE INDEX "groups_group_created_by_id_498c8e85" ON "groups_group" ("created_by_id");

CREATE INDEX "groups_group_updated_by_id_57f18485" ON "groups_group" ("updated_by_id");

ALTER TABLE "groups_groupmessage" ADD CONSTRAINT "groups_groupmessage_created_by_id_d1953350_fk_users_user_uuid" FOREIGN KEY ("created_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_groupmessage" ADD CONSTRAINT "groups_groupmessage_group_id_cf48fa26_fk_groups_group_id" FOREIGN KEY ("group_id") REFERENCES "groups_group" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_groupmessage" ADD CONSTRAINT "groups_groupmessage_updated_by_id_bc0798af_fk_users_user_uuid" FOREIGN KEY ("updated_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "groups_groupmessage_created_by_id_d1953350" ON "groups_groupmessage" ("created_by_id");

CREATE INDEX "groups_groupmessage_group_id_cf48fa26" ON "groups_groupmessage" ("group_id");

CREATE INDEX "groups_groupmessage_updated_by_id_bc0798af" ON "groups_groupmessage" ("updated_by_id");

ALTER TABLE "groups_groupmember" ADD CONSTRAINT "groups_groupmember_created_by_id_7fc5ec84_fk_users_user_uuid" FOREIGN KEY ("created_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_groupmember" ADD CONSTRAINT "groups_groupmember_group_id_1c1b676d_fk_groups_group_id" FOREIGN KEY ("group_id") REFERENCES "groups_group" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_groupmember" ADD CONSTRAINT "groups_groupmember_updated_by_id_c0fdf5a9_fk_users_user_uuid" FOREIGN KEY ("updated_by_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "groups_groupmember" ADD CONSTRAINT "groups_groupmember_user_id_f9e9f041_fk_users_user_uuid" FOREIGN KEY ("user_id") REFERENCES "users_user" ("uuid") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "groups_groupmember_created_by_id_7fc5ec84" ON "groups_groupmember" ("created_by_id");

CREATE INDEX "groups_groupmember_group_id_1c1b676d" ON "groups_groupmember" ("group_id");

CREATE INDEX "groups_groupmember_updated_by_id_c0fdf5a9" ON "groups_groupmember" ("updated_by_id");

CREATE INDEX "groups_groupmember_user_id_f9e9f041" ON "groups_groupmember" ("user_id");

COMMIT;