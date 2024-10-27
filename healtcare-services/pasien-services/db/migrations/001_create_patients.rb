Sequel.migration do
    change do
      create_table(:patients) do
        primary_key :id
        String :name
        String :age
        String :contact_info
      end
    end
  end
  