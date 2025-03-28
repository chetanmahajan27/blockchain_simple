import snowflake.connector
import os

def get_snowflake_ddl_with_comments_and_constraints(account, user, password, warehouse, database, schema, table_names, target_account, target_user, target_password, target_warehouse, target_database, target_schema):
    """
    Retrieves DDL for Snowflake tables, including column comments and constraints,
    and executes them on a target Snowflake database.

    Args:
        account (str): Snowflake account name.
        user (str): Snowflake user name.
        password (str): Snowflake password.
        warehouse (str): Snowflake warehouse name.
        database (str): Snowflake database name.
        schema (str): Snowflake schema name.
        table_names (list): List of table names.
        target_account (str): Target Snowflake account name.
        target_user (str): Target Snowflake user name.
        target_password (str): Target Snowflake password.
        target_warehouse (str): Target Snowflake warehouse name.
        target_database (str): Target Snowflake database name.
        target_schema (str): Target Snowflake schema name.
    """

    try:
        # Connect to the source Snowflake database
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema,
        )
        cur = conn.cursor()

        # Connect to the target Snowflake database
        target_conn = snowflake.connector.connect(
            account=target_account,
            user=target_user,
            password=target_password,
            warehouse=target_warehouse,
            database=target_database,
            schema=target_schema,
        )
        target_cur = target_conn.cursor()

        for table_name in table_names:
            try:
                # Get the CREATE TABLE statement
                cur.execute(f"SHOW CREATE TABLE {table_name}")
                create_table_result = cur.fetchone()
                create_table_statement = create_table_result[0]

                # Get column comments
                cur.execute(f"SHOW COLUMNS IN {table_name}")
                columns = cur.fetchall()
                column_comments = {}
                for column in columns:
                    if column[6]:  # Column comment
                        column_comments[column[1]] = column[6]

                # Reconstruct the CREATE TABLE statement with comments
                for column_name, comment in column_comments.items():
                    create_table_statement = create_table_statement.replace(
                        f'"{column_name}"', f'"{column_name}" COMMENT \'{comment}\''
                    )

                # Get constraints.
                cur.execute(f"SHOW PRIMARY KEYS IN TABLE {table_name}")
                primary_keys = cur.fetchall()
                primary_key_constraints = []
                for pk in primary_keys:
                    primary_key_constraints.append(pk[2])

                cur.execute(f"SHOW UNIQUE KEYS IN TABLE {table_name}")
                unique_keys = cur.fetchall()
                unique_key_constraints = []
                for uk in unique_keys:
                    unique_key_constraints.append(uk[2])

                cur.execute(f"SHOW FOREIGN KEYS IN TABLE {table_name}")
                foreign_keys = cur.fetchall()
                foreign_key_constraints = []
                for fk in foreign_keys:
                    foreign_key_constraints.append(fk[2])

                # Execute the CREATE TABLE statement on the target database
                target_cur.execute(create_table_statement)

                # Execute constraints on the target database.
                for constraint in primary_key_constraints:
                    target_cur.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint}")
                for constraint in unique_key_constraints:
                    target_cur.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint}")
                for constraint in foreign_key_constraints:
                    target_cur.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint}")

                print(f"Table '{table_name}' created successfully in {target_database}.{target_schema}.")

            except snowflake.connector.errors.ProgrammingError as e:
                print(f"Error processing table '{table_name}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred processing table '{table_name}': {e}")

        # Close connections
        cur.close()
        conn.close()
        target_cur.close()
        target_conn.close()

    except snowflake.connector.errors.Error as e:
        print(f"Snowflake connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (replace with your Snowflake credentials and table names):
source_account = os.environ.get("SNOWFLAKE_ACCOUNT")
source_user = os.environ.get("SNOWFLAKE_USER")
source_password = os.environ.get("SNOWFLAKE_PASSWORD")
source_warehouse = "COMPUTE_WH"
source_database = "SOURCE_DB"
source_schema = "PUBLIC"

target_account = os.environ.get("TARGET_SNOWFLAKE_ACCOUNT")
target_user = os.environ.get("TARGET_SNOWFLAKE_USER")
target_password = os.environ.get("TARGET_SNOWFLAKE_PASSWORD")
target_warehouse = "COMPUTE_WH"
target_database = "TARGET_DB"
target_schema = "PUBLIC"

table_names = ["TABLE1", "TABLE2", "TABLE3"]  # Replace with your table names

get_snowflake_ddl_with_comments_and_constraints(
    source_account,
    source_user,
    source_password,
    source_warehouse,
    source_database,
    source_schema,
    table_names,
    target_account,
    target_user,
    target_password,
    target_warehouse,
    target_database,
    target_schema,
)
