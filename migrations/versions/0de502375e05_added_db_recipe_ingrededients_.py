"""added db Recipe, Ingrededients, Instruction

Revision ID: 0de502375e05
Revises: 49fa51a1c659
Create Date: 2024-09-14 12:50:14.913250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0de502375e05'
down_revision = '49fa51a1c659'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipe_author_id'), ['author_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_recipe_name'), ['name'], unique=False)

    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ingredients_amount'), ['amount'], unique=False)
        batch_op.create_index(batch_op.f('ix_ingredients_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_ingredients_recipe_id'), ['recipe_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_ingredients_unit'), ['unit'], unique=False)

    op.create_table('instruction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('tasks', sa.String(length=5000), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('instruction', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_instruction_recipe_id'), ['recipe_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_instruction_tasks'), ['tasks'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instruction', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_instruction_tasks'))
        batch_op.drop_index(batch_op.f('ix_instruction_recipe_id'))

    op.drop_table('instruction')
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ingredients_unit'))
        batch_op.drop_index(batch_op.f('ix_ingredients_recipe_id'))
        batch_op.drop_index(batch_op.f('ix_ingredients_name'))
        batch_op.drop_index(batch_op.f('ix_ingredients_amount'))

    op.drop_table('ingredients')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipe_name'))
        batch_op.drop_index(batch_op.f('ix_recipe_author_id'))

    op.drop_table('recipe')
    # ### end Alembic commands ###
