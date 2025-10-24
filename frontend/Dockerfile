# ============================
# # 1️⃣ BUILD STAGE
# # ============================
# FROM node:20-alpine AS builder

# # Set working directory
# WORKDIR /app

# # Copy package files first for caching
# COPY package*.json ./

# # Install dependencies
# RUN npm install --legacy-peer-deps

# # Copy all files
# COPY . .

# # Build the Next.js app
# RUN npm run build

# # ============================
# # 2️⃣ RUN STAGE
# # ============================
# FROM node:20-alpine AS runner

# WORKDIR /app

# # Copy only necessary files from builder
# COPY --from=builder /app/package*.json ./
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/node_modules ./node_modules

# # Expose the Next.js port
# EXPOSE 3000

# # Define environment
# ENV NODE_ENV=production

# # Start Next.js app
# CMD ["npm", 'run',"dev"]



FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .

# Next.js dev server (with live reload)
EXPOSE 3000
CMD ["npm", "run", "dev"]
