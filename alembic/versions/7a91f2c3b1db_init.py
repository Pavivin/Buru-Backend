"""init

Revision ID: 7a91f2c3b1db
Revises: 
Create Date: 2021-12-28 11:32:42.740775

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a91f2c3b1db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TYPE offertype AS ENUM (
            'LOW',
            'MEDIUM',
            'HIGH',
            'HIGHEST',
            'SUPER'
        );

        CREATE TYPE promostatus AS ENUM (
            'CREATED',
            'GRANTED',
            'OPEN'
        );

        CREATE TABLE public.users (
            user_id uuid NOT NULL,
            created_at timestamptz NOT NULL,
            email varchar NOT NULL,
            hash_pass varchar NOT NULL,
            CONSTRAINT users_pkey PRIMARY KEY (user_id)
        );

        CREATE TABLE public.offer (
            offer_id uuid NOT NULL,
            offer_type offertype NOT NULL,
            title varchar NOT NULL,
            restrictions varchar NULL,
            promosite_url varchar NOT NULL,
            img_url varchar NOT NULL,
            hash_img varchar NULL,
            created_at timestamptz NOT NULL,
            CONSTRAINT offer_pkey PRIMARY KEY (offer_id)
        );

        CREATE TABLE public.promocode (
            promo_id uuid NOT NULL,
            offer_id uuid NOT NULL REFERENCES public.offer(offer_id),
            status promostatus NOT NULL,
            promo_code varchar NOT NULL,
            cur_count int default 1 CONSTRAINT positive_count CHECK (cur_count > 0),
            created_at timestamptz NOT NULL,
            updated_at timestamptz NULL,
            deleted_at timestamptz NULL,
            user_id uuid NULL,
            expired_at timestamptz,
            CONSTRAINT promo_code_pkey PRIMARY KEY (promo_id),
            CONSTRAINT promo_code_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL ON UPDATE SET NULL
        );

        CREATE TABLE public.referal_promo (
            id uuid NOT NULL,
            user_id uuid NOT NULL,
            friend_count int4 NOT NULL,
            created_at timestamptz NOT NULL,
            CONSTRAINT referal_promo_pkey PRIMARY KEY (id, user_id),
            CONSTRAINT referal_promo_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL ON UPDATE SET NULL
        );

        CREATE TABLE public.user_promo (
            id uuid NOT NULL,
            user_id uuid NOT NULL,
            promo_id uuid NOT NULL,
            created_at timestamptz NOT NULL,
            CONSTRAINT user_promo_pkey PRIMARY KEY (promo_id),
            CONSTRAINT user_promo_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL ON UPDATE SET NULL
        );

        CREATE TABLE user_sessions (
            id uuid NOT NULL,
            user_id uuid NOT NULL,
            expires_at timestamp,
            CONSTRAINT user_sessions_pkey PRIMARY KEY (id)
        );
    """)


def downgrade():
    op.execute("""
        DROP TYPE IF EXISTS offertype;
        DROP TYPE IF EXISTS promostatus;
        DROP TABLE IF EXISTS offer;
        DROP TABLE IF EXISTS promo_code;
        DROP TABLE IF EXISTS referal_promo;
        DROP TABLE IF EXISTS user_promo;
        DROP TABLE IF EXISTS promostatus;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS assistant;
        DROP TABLE IF EXISTS offertype;
        DROP TABLE IF EXISTS user_sessions;
    """)
